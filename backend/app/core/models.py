"""Data structures shared by the analyzer and the rules."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal

Severity = Literal["low", "medium", "high"]
Verdict = Literal["safe", "suspicious", "dangerous"]


@dataclass(frozen=True)
class ParsedUrl:
    raw: str
    normalized: str
    scheme: str
    had_scheme: bool
    host: str  # lower-case ASCII (punycode) form
    host_display: str  # decoded Unicode form
    port: int | None
    path: str
    query: str
    userinfo: str
    subdomain: str
    registered_domain: str
    suffix: str
    label: str  # registered domain without suffix, e.g. "paypal"
    ip: str | None


@dataclass
class Finding:
    rule_id: str
    severity: Severity
    weight: int
    title: dict[str, str]
    detail: dict[str, str]
    evidence: str = ""


@dataclass
class AnalysisResult:
    url: str
    normalized_url: str
    scheme: str
    host: str
    host_display: str
    subdomain: str
    registered_domain: str
    suffix: str
    path: str
    score: int
    verdict: Verdict
    findings: list[Finding] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
