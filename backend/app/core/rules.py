"""Heuristic detection rules. Each rule returns a Finding or None."""

from __future__ import annotations

import re
from collections.abc import Callable
from urllib.parse import unquote

from . import data
from .domain import scripts_in
from .messages import render
from .models import Finding, ParsedUrl, Severity

Rule = Callable[[ParsedUrl], Finding | None]

_TOKEN_SPLIT = re.compile(r"[.\-_/@:?=&+~]+")
_PERCENT = re.compile(r"%[0-9a-fA-F]{2}")

# Words that phishers glue onto brand names (paypalsecure, applesupport, ...).
_PHISH_AFFIXES = {
    "secure", "security", "login", "signin", "verify", "verification", "account", "accounts",
    "support", "service", "services", "help", "helpdesk", "online", "update", "updates", "id",
    "app", "web", "mail", "pay", "payment", "billing", "center", "centre", "auth", "confirm",
    "team", "official", "customer", "care", "alert", "alerts", "unlock", "recovery", "wallet",
}

# Characters commonly swapped in look-alike domains, mapped to the letter they imitate.
_HOMOGLYPHS = {
    "0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "7": "t", "8": "b", "@": "a", "$": "s",
    # Cyrillic / Greek letters that render like Latin ones.
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y", "х": "x", "і": "i", "ј": "j",
    "ѕ": "s", "ԁ": "d", "ɡ": "g", "һ": "h", "ӏ": "l", "ο": "o", "α": "a", "ν": "v", "τ": "t",
    "κ": "k", "ι": "i", "ρ": "p",
}
_MULTI_GLYPHS = (("rn", "m"), ("vv", "w"), ("cl", "d"))


def _finding(rule_id: str, severity: Severity, weight: int, evidence: str = "", **params) -> Finding:
    texts = render(rule_id, evidence=evidence, **params)
    return Finding(rule_id, severity, weight, texts["title"], texts["detail"], evidence)


def _official(registered_domain: str, host: str, brand: str) -> bool:
    for domain in data.BRANDS[brand]:
        if registered_domain == domain or host == domain or host.endswith("." + domain):
            return True
    return False


def _is_any_official(url: ParsedUrl) -> bool:
    return any(_official(url.registered_domain, url.host, b) for b in data.BRANDS)


def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if abs(len(a) - len(b)) > 2:
        return 3
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _deglyph(token: str) -> str:
    out = "".join(_HOMOGLYPHS.get(ch, ch) for ch in token)
    for src, dst in _MULTI_GLYPHS:
        out = out.replace(src, dst)
    return out


def _host_tokens(url: ParsedUrl) -> list[str]:
    parts = [url.host_display, url.userinfo]
    return [t for p in parts for t in _TOKEN_SPLIT.split(p.lower()) if t]


def _brand_in_token(token: str, brand: str) -> bool:
    if token == brand:
        return True
    if brand in data.SHORT_BRANDS or brand not in token:
        return False
    rest = token.replace(brand, "", 1)
    return rest.isdigit() or rest in _PHISH_AFFIXES


# --- high severity ---------------------------------------------------------

def ip_address(url: ParsedUrl) -> Finding | None:
    if url.ip:
        # Decimal / hex / octal notations exist only to disguise the address.
        obfuscated = url.host.strip("[]") != url.ip
        return _finding("ip_address", "high", 55 if obfuscated else 40, url.ip)
    return None


def at_symbol(url: ParsedUrl) -> Finding | None:
    if url.userinfo:
        return _finding("at_symbol", "high", 45, url.host_display)
    return None


def punycode(url: ParsedUrl) -> Finding | None:
    if "xn--" in url.host:
        return _finding("punycode", "medium", 25, url.host_display)
    return None


def mixed_script(url: ParsedUrl) -> Finding | None:
    for label in url.host_display.split("."):
        scripts = scripts_in(label)
        if len(scripts) > 1:
            return _finding("mixed_script", "high", 45, " + ".join(sorted(scripts)))
    return None


def brand_impersonation(url: ParsedUrl) -> Finding | None:
    if url.ip is None and _is_any_official(url):
        return None
    tokens = _host_tokens(url)
    for brand in data.BRANDS:
        if any(_brand_in_token(t, brand) for t in tokens):
            return _finding("brand_impersonation", "high", 45, brand, domain=url.registered_domain or url.host)

    # Brand only in the path: suspicious when combined with credential-related words.
    path = unquote(url.path + "?" + url.query).lower()
    path_tokens = set(_TOKEN_SPLIT.split(path))
    if any(k in path for k in data.SENSITIVE_KEYWORDS):
        for brand in data.BRANDS:
            if brand in path_tokens:
                return _finding("brand_impersonation", "high", 25, brand, domain=url.registered_domain or url.host)
    return None


def typosquatting(url: ParsedUrl) -> Finding | None:
    if url.ip or _is_any_official(url):
        return None
    candidates = {url.label.lower()} | set(_TOKEN_SPLIT.split(url.label.lower()))
    candidates |= set(_TOKEN_SPLIT.split(url.subdomain.lower())) if url.subdomain else set()
    display_label = url.host_display.split(".")
    candidates |= {lbl.lower() for lbl in display_label}
    for token in candidates:
        if len(token) < 4:
            continue
        cleaned = _deglyph(token)
        for brand in data.TYPO_TARGETS:
            if token == brand:
                continue
            if cleaned == brand:
                return _finding("typosquatting", "high", 60, token, brand=brand)
            distance = _levenshtein(cleaned, brand)
            if (len(brand) >= 6 and distance == 1) or (len(brand) >= 9 and distance == 2):
                return _finding("typosquatting", "high", 60, token, brand=brand)
    return None


# --- medium severity -------------------------------------------------------

def suspicious_tld(url: ParsedUrl) -> Finding | None:
    tld = url.suffix.rsplit(".", 1)[-1]
    if not url.ip and tld in data.SUSPICIOUS_TLDS:
        return _finding("suspicious_tld", "medium", 15, tld)
    return None


def shortener(url: ParsedUrl) -> Finding | None:
    if url.registered_domain in data.SHORTENERS or url.host in data.SHORTENERS:
        return _finding("shortener", "medium", 30, url.host)
    return None


def many_subdomains(url: ParsedUrl) -> Finding | None:
    if url.ip or not url.subdomain:
        return None
    levels = [s for s in url.subdomain.split(".") if s and s != "www"]
    if len(levels) >= 3:
        return _finding("many_subdomains", "medium", 15, str(len(levels)))
    return None


def non_standard_port(url: ParsedUrl) -> Finding | None:
    if url.port is not None and url.port != data.DEFAULT_PORTS.get(url.scheme):
        return _finding("non_standard_port", "medium", 15, str(url.port))
    return None


def embedded_redirect(url: ParsedUrl) -> Finding | None:
    path = url.path
    if "//" in path[1:]:
        return _finding("embedded_redirect", "medium", 15, path[path.index("//", 1):][:60])
    query = unquote(url.query)
    match = re.search(r"(https?://|www\.)[^\s&]+", query, re.IGNORECASE)
    if match:
        return _finding("embedded_redirect", "medium", 15, match.group(0)[:60])
    return None


def https_in_domain(url: ParsedUrl) -> Finding | None:
    for token in _TOKEN_SPLIT.split(url.host):
        if token.startswith("http"):
            return _finding("https_in_domain", "medium", 20, token)
    return None


def dangerous_file(url: ParsedUrl) -> Finding | None:
    path = url.path.lower()
    for ext in data.DANGEROUS_EXTENSIONS:
        if path.endswith(ext):
            return _finding("dangerous_file", "medium", 25, ext)
    return None


# --- low severity ----------------------------------------------------------

def many_hyphens(url: ParsedUrl) -> Finding | None:
    count = (url.subdomain + "." + url.label).count("-")
    if count >= 3:
        return _finding("many_hyphens", "low", 10, str(count))
    return None


def sensitive_keywords(url: ParsedUrl) -> Finding | None:
    text = unquote(url.normalized).lower()
    found = [k for k in data.SENSITIVE_KEYWORDS if k in text]
    # Prefer the longest match when keywords overlap (e.g. "verify" inside "verification").
    found = [k for k in found if not any(k != o and k in o for o in found)]
    if found:
        return _finding("sensitive_keywords", "low", min(15, 5 * len(found)), ", ".join(found[:5]))
    return None


def long_url(url: ParsedUrl) -> Finding | None:
    length = len(url.normalized)
    if length > 120:
        return _finding("long_url", "low", 10, str(length))
    if length > 75:
        return _finding("long_url", "low", 5, str(length))
    return None


def no_https(url: ParsedUrl) -> Finding | None:
    if url.had_scheme and url.scheme == "http":
        return _finding("no_https", "low", 8, "http")
    return None


def obfuscation(url: ParsedUrl) -> Finding | None:
    count = len(_PERCENT.findall(url.normalized))
    if count >= 5:
        return _finding("obfuscation", "low", 10, str(count))
    return None


ALL_RULES: tuple[Rule, ...] = (
    ip_address,
    at_symbol,
    punycode,
    mixed_script,
    brand_impersonation,
    typosquatting,
    suspicious_tld,
    shortener,
    many_subdomains,
    non_standard_port,
    embedded_redirect,
    https_in_domain,
    dangerous_file,
    many_hyphens,
    sensitive_keywords,
    long_url,
    no_https,
    obfuscation,
)
