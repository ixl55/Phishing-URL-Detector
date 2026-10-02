"""Hostname helpers: IP detection, registered-domain extraction and IDN handling."""

from __future__ import annotations

import ipaddress
import re
import unicodedata

from .data import MULTI_PART_SUFFIXES

_HEX_OR_OCT_PART = re.compile(r"^(0x[0-9a-f]+|0[0-7]*|[1-9][0-9]*)$", re.IGNORECASE)


def _parse_ip_part(part: str) -> int | None:
    if not _HEX_OR_OCT_PART.match(part):
        return None
    if part.lower().startswith("0x"):
        return int(part, 16)
    if len(part) > 1 and part.startswith("0"):
        return int(part, 8)
    return int(part)


def parse_ip(host: str) -> str | None:
    """Return the canonical IP if *host* is an IP address in any common notation.

    Handles dotted IPv4, IPv6 (with or without brackets) and the obfuscated forms
    browsers still accept: a single decimal integer, hex (0xC0A80001) and octal parts.
    """
    if not host:
        return None
    candidate = host.strip("[]")
    try:
        return str(ipaddress.ip_address(candidate))
    except ValueError:
        pass

    parts = candidate.split(".")
    if not 1 <= len(parts) <= 4:
        return None
    values = [_parse_ip_part(p) for p in parts]
    if any(v is None for v in values):
        return None

    # inet_aton semantics: the last part fills the remaining bytes.
    *head, last = values
    if any(v > 255 for v in head) or last >= 256 ** (4 - len(head)):
        return None
    number = 0
    for v in head:
        number = number * 256 + v
    number = number * 256 ** (4 - len(head)) + last
    return str(ipaddress.IPv4Address(number))


def split_host(host: str) -> tuple[str, str, str]:
    """Split *host* into (subdomain, registered_domain, suffix)."""
    labels = [label for label in host.split(".") if label]
    if len(labels) < 2:
        return "", host, ""
    two = ".".join(labels[-2:])
    if two in MULTI_PART_SUFFIXES and len(labels) >= 3:
        suffix = two
        registered = ".".join(labels[-3:])
        sub = labels[:-3]
    else:
        suffix = labels[-1]
        registered = two
        sub = labels[:-2]
    return ".".join(sub), registered, suffix


def domain_label(registered_domain: str, suffix: str) -> str:
    """The registrable label without its suffix, e.g. ``paypal`` for ``paypal.com``."""
    if suffix and registered_domain.endswith("." + suffix):
        return registered_domain[: -len(suffix) - 1]
    return registered_domain.split(".")[0]


def decode_idna(host: str) -> str:
    """Decode punycode labels (xn--) for display; leave invalid labels untouched."""
    out = []
    for label in host.split("."):
        if label.startswith("xn--"):
            try:
                out.append(label.encode("ascii").decode("idna"))
                continue
            except UnicodeError:
                pass
        out.append(label)
    return ".".join(out)


def scripts_in(text: str) -> set[str]:
    """Return the set of Unicode scripts (by name prefix) used by letters in *text*."""
    scripts = set()
    for ch in text:
        if not ch.isalpha():
            continue
        try:
            name = unicodedata.name(ch)
        except ValueError:
            continue
        scripts.add(name.split(" ")[0])
    return scripts
