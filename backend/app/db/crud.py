from collections import Counter

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from ..core.models import AnalysisResult
from .models import Scan


def save_scan(session: Session, result: AnalysisResult, source: str = "single") -> Scan:
    scan = Scan(
        url=result.url,
        normalized_url=result.normalized_url,
        host=result.host_display or result.host,
        score=result.score,
        verdict=result.verdict,
        findings=result.to_dict()["findings"],
        source=source,
    )
    session.add(scan)
    session.commit()
    return scan


def list_scans(session: Session, limit: int, offset: int, verdict: str | None) -> tuple[list[Scan], int]:
    query = select(Scan)
    count = select(func.count(Scan.id))
    if verdict:
        query = query.where(Scan.verdict == verdict)
        count = count.where(Scan.verdict == verdict)
    items = session.scalars(query.order_by(Scan.id.desc()).limit(limit).offset(offset)).all()
    return list(items), session.scalar(count) or 0


def delete_scan(session: Session, scan_id: int) -> bool:
    deleted = session.execute(delete(Scan).where(Scan.id == scan_id)).rowcount
    session.commit()
    return bool(deleted)


def clear_scans(session: Session) -> int:
    deleted = session.execute(delete(Scan)).rowcount
    session.commit()
    return deleted


def stats(session: Session, top: int = 8) -> dict:
    by_verdict = dict(session.execute(select(Scan.verdict, func.count(Scan.id)).group_by(Scan.verdict)).all())
    rule_counter: Counter[str] = Counter()
    rule_titles: dict[str, dict] = {}
    for findings in session.scalars(select(Scan.findings)):
        for f in findings or []:
            rule_counter[f["rule_id"]] += 1
            rule_titles.setdefault(f["rule_id"], f["title"])
    return {
        "total": sum(by_verdict.values()),
        "safe": by_verdict.get("safe", 0),
        "suspicious": by_verdict.get("suspicious", 0),
        "dangerous": by_verdict.get("dangerous", 0),
        "top_rules": [
            {"rule_id": rule_id, "title": rule_titles[rule_id], "count": n}
            for rule_id, n in rule_counter.most_common(top)
        ],
    }
