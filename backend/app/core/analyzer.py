"""URL parsing, rule execution, scoring and verdict."""

from __future__ import annotations

import re
from urllib.parse import urlsplit, urlunsplit

from .domain import decode_idna, domain_label, parse_ip, split_host
from .messages import render
from .models import AnalysisResult, Finding, ParsedUrl, Verdict
from .rules import ALL_RULES

SAFE_BELOW = 30
DANGEROUS_FROM = 60

_SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://")
_OPAQUE_SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+\-]*:(?!\d)")  # mailto:, tel:, ... (not host:port)
_DANGEROUS_SCHEMES = ("javascript:", "data:", "vbscript:")
_HOST_CHARS = re.compile(r"^[a-z0-9.\-_\[\]:]+$")


class InvalidUrlError(ValueError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def parse_url(raw: str) -> ParsedUrl:
    text = (raw or "").strip()
    if not text:
        raise InvalidUrlError("empty")
    if any(ch.isspace() for ch in text):
        raise InvalidUrlError("invalid")

    had_scheme = bool(_SCHEME.match(text))
    if not had_scheme and _OPAQUE_SCHEME.match(text):
        raise InvalidUrlError("invalid")
    candidate = text if had_scheme else "http://" + text.lstrip("/")
    parts = urlsplit(candidate)
    scheme = parts.scheme.lower()
    if scheme not in ("http", "https", "ftp"):
        raise InvalidUrlError("invalid")

    try:
        port = parts.port
    except ValueError as exc:
        raise InvalidUrlError("invalid") from exc

    hostname = (parts.hostname or "").rstrip(".")
    if not hostname:
        raise InvalidUrlError("invalid")
    try:
        host_ascii = hostname.encode("idna").decode("ascii").lower()
    except UnicodeError:
        host_ascii = hostname.lower()
    if not _HOST_CHARS.match(host_ascii):
        raise InvalidUrlError("invalid")

    ip = parse_ip(host_ascii)
    if ip is None and "." not in host_ascii and host_ascii != "localhost":
        raise InvalidUrlError("invalid")

    userinfo = parts.netloc.rsplit("@", 1)[0] if "@" in parts.netloc else ""
    if ip:
        subdomain, registered, suffix, label = "", ip, "", ip
    else:
        subdomain, registered, suffix = split_host(host_ascii)
        label = domain_label(registered, suffix)

    netloc = parts.netloc.lower() if not userinfo else parts.netloc
    normalized = urlunsplit((scheme, netloc, parts.path, parts.query, parts.fragment))

    return ParsedUrl(
        raw=text,
        normalized=normalized,
        scheme=scheme,
        had_scheme=had_scheme,
        host=host_ascii,
        host_display=decode_idna(host_ascii),
        port=port,
        path=parts.path,
        query=parts.query,
        userinfo=userinfo,
        subdomain=subdomain,
        registered_domain=registered,
        suffix=suffix,
        label=label,
        ip=ip,
    )


def verdict_for(score: int, findings: list[Finding]) -> Verdict:
    if score >= DANGEROUS_FROM:
        return "dangerous"
    if score >= SAFE_BELOW or any(f.severity == "high" for f in findings):
        return "suspicious"
    return "safe"


def _dangerous_scheme_result(text: str) -> AnalysisResult:
    scheme = text.split(":", 1)[0].lower()
    texts = render("dangerous_scheme", evidence=scheme + ":")
    finding = Finding("dangerous_scheme", "high", 100, texts["title"], texts["detail"], scheme + ":")
    return AnalysisResult(
        url=text, normalized_url=text[:200], scheme=scheme, host="", host_display="", subdomain="",
        registered_domain="", suffix="", path="", score=100, verdict="dangerous", findings=[finding],
    )


def analyze_url(raw: str) -> AnalysisResult:
    """Analyze *raw* and return a scored result. Raises InvalidUrlError for bad input."""
    text = (raw or "").strip()
    if text.lower().startswith(_DANGEROUS_SCHEMES):
        return _dangerous_scheme_result(text)

    url = parse_url(text)
    findings = [f for rule in ALL_RULES if (f := rule(url)) is not None]
    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (order[f.severity], -f.weight))
    score = min(100, sum(f.weight for f in findings))

    return AnalysisResult(
        url=url.raw,
        normalized_url=url.normalized,
        scheme=url.scheme,
        host=url.host,
        host_display=url.host_display,
        subdomain=url.subdomain,
        registered_domain=url.registered_domain,
        suffix=url.suffix,
        path=url.path + (("?" + url.query) if url.query else ""),
        score=score,
        verdict=verdict_for(score, findings),
        findings=findings,
    )
