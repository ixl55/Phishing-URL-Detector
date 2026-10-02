from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Severity = Literal["low", "medium", "high"]
VerdictName = Literal["safe", "suspicious", "dangerous"]


class LocalizedText(BaseModel):
    ar: str
    en: str


class FindingOut(BaseModel):
    rule_id: str
    severity: Severity
    weight: int
    title: LocalizedText
    detail: LocalizedText
    evidence: str


class AnalyzeRequest(BaseModel):
    url: str = Field(..., max_length=4096)


class AnalysisOut(BaseModel):
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
    verdict: VerdictName
    verdict_label: LocalizedText
    advice: LocalizedText
    findings: list[FindingOut]


class BatchRequest(BaseModel):
    text: str | None = Field(default=None, max_length=50_000)
    urls: list[str] | None = None

    @model_validator(mode="after")
    def _one_source(self) -> "BatchRequest":
        if not (self.text and self.text.strip()) and not self.urls:
            raise ValueError("Provide 'text' or 'urls'.")
        return self


class BatchItem(BaseModel):
    input: str
    result: AnalysisOut | None = None
    error: LocalizedText | None = None


class BatchSummary(BaseModel):
    total: int
    safe: int
    suspicious: int
    dangerous: int
    invalid: int


class BatchResponse(BaseModel):
    items: list[BatchItem]
    summary: BatchSummary


class ScanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    normalized_url: str
    host: str
    score: int
    verdict: VerdictName
    findings: list[FindingOut]
    source: str
    created_at: datetime


class HistoryPage(BaseModel):
    items: list[ScanOut]
    total: int
    limit: int
    offset: int


class RuleCount(BaseModel):
    rule_id: str
    title: LocalizedText
    count: int


class StatsOut(BaseModel):
    total: int
    safe: int
    suspicious: int
    dangerous: int
    top_rules: list[RuleCount]
