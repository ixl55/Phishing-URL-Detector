from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..config import settings
from ..core.analyzer import InvalidUrlError, analyze_url
from ..core.extractor import extract_urls
from ..core.messages import ERRORS, VERDICT_ADVICE, VERDICT_LABELS
from ..core.models import AnalysisResult
from ..db import crud
from ..db.database import get_session
from ..schemas import AnalysisOut, AnalyzeRequest, BatchItem, BatchRequest, BatchResponse, BatchSummary

router = APIRouter(prefix="/api", tags=["analyze"])


def to_out(result: AnalysisResult) -> AnalysisOut:
    return AnalysisOut(
        **result.to_dict(),
        verdict_label=VERDICT_LABELS[result.verdict],
        advice=VERDICT_ADVICE[result.verdict],
    )


@router.post("/analyze", response_model=AnalysisOut)
def analyze(body: AnalyzeRequest, session: Session = Depends(get_session)) -> AnalysisOut:
    try:
        result = analyze_url(body.url)
    except InvalidUrlError as exc:
        raise HTTPException(status_code=422, detail={"code": exc.code, "message": ERRORS[exc.code]}) from exc
    crud.save_scan(session, result, source="single")
    return to_out(result)


@router.post("/analyze/batch", response_model=BatchResponse)
def analyze_batch(body: BatchRequest, session: Session = Depends(get_session)) -> BatchResponse:
    inputs = [u.strip() for u in (body.urls or []) if u.strip()] or extract_urls(body.text or "", settings.max_batch)
    inputs = inputs[: settings.max_batch]
    if not inputs:
        raise HTTPException(status_code=422, detail={"code": "no_urls", "message": ERRORS["no_urls"]})

    items: list[BatchItem] = []
    counts = {"safe": 0, "suspicious": 0, "dangerous": 0, "invalid": 0}
    for raw in inputs:
        try:
            result = analyze_url(raw)
        except InvalidUrlError as exc:
            counts["invalid"] += 1
            items.append(BatchItem(input=raw, error=ERRORS[exc.code]))
            continue
        crud.save_scan(session, result, source="batch")
        counts[result.verdict] += 1
        items.append(BatchItem(input=raw, result=to_out(result)))

    return BatchResponse(items=items, summary=BatchSummary(total=len(items), **counts))
