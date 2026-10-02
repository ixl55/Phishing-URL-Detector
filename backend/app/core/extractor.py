"""Extract URLs from free text such as an SMS or an e-mail body."""

from __future__ import annotations

import re

_DEFANG = (
    (re.compile(r"\bhxxps\b", re.IGNORECASE), "https"),
    (re.compile(r"\bhxxp\b", re.IGNORECASE), "http"),
    (re.compile(r"\[\.\]|\(\.\)|\{\.\}|\[dot\]", re.IGNORECASE), "."),
    (re.compile(r"\[:\]"), ":"),
    (re.compile(r"\[/\]"), "/"),
)

_URL = re.compile(
    r"""(?:
        (?:https?|ftp)://[^\s<>"'`]+          # explicit scheme
      | www\.[^\s<>"'`]+                       # www. prefix
      | (?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.)+[a-z]{2,24}(?::\d{2,5})?/[^\s<>"'`]*  # bare domain + path
    )""",
    re.IGNORECASE | re.VERBOSE,
)

_TRAILING = ".,;:!?)]}>'\"،؛؟»"


def refang(text: str) -> str:
    for pattern, replacement in _DEFANG:
        text = pattern.sub(replacement, text)
    return text


def extract_urls(text: str, limit: int = 50) -> list[str]:
    """Return unique URLs found in *text*, in order of appearance."""
    seen: set[str] = set()
    urls: list[str] = []
    for match in _URL.finditer(refang(text or "")):
        url = match.group(0).rstrip(_TRAILING)
        if url.count("(") < url.count(")"):
            url = url.rstrip(")")
        key = url.lower()
        if url and key not in seen:
            seen.add(key)
            urls.append(url)
            if len(urls) >= limit:
                break
    return urls
