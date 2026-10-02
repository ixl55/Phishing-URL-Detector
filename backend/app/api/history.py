from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import crud
from ..db.database import get_session
from ..schemas import HistoryPage, ScanOut, StatsOut

router = APIRouter(prefix="/api", tags=["history"])


@router.get("/history", response_model=HistoryPage)
def history(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    verdict: Literal["safe", "suspicious", "dangerous"] | None = None,
    session: Session = Depends(get_session),
) -> HistoryPage:
    items, total = crud.list_scans(session, limit, offset, verdict)
    return HistoryPage(items=[ScanOut.model_validate(i) for i in items], total=total, limit=limit, offset=offset)


@router.delete("/history/{scan_id}", status_code=204)
def delete_scan(scan_id: int, session: Session = Depends(get_session)) -> None:
    if not crud.delete_scan(session, scan_id):
        raise HTTPException(status_code=404, detail="Scan not found")


@router.delete("/history")
def clear_history(session: Session = Depends(get_session)) -> dict:
    return {"deleted": crud.clear_scans(session)}


@router.get("/stats", response_model=StatsOut)
def stats(session: Session = Depends(get_session)) -> StatsOut:
    return StatsOut(**crud.stats(session))
