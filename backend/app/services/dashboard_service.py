from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.screening import ScreeningRecord


def _period_start(days: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days)


def get_dashboard_stats(db: Session) -> dict:
    total_resumes = db.query(func.count(Candidate.id)).scalar() or 0

    resumes_today = (
        db.query(func.count(Candidate.id))
        .filter(Candidate.created_at >= _period_start(1))
        .scalar()
        or 0
    )
    resumes_this_week = (
        db.query(func.count(Candidate.id))
        .filter(Candidate.created_at >= _period_start(7))
        .scalar()
        or 0
    )
    resumes_this_month = (
        db.query(func.count(Candidate.id))
        .filter(Candidate.created_at >= _period_start(30))
        .scalar()
        or 0
    )
    resumes_this_year = (
        db.query(func.count(Candidate.id))
        .filter(Candidate.created_at >= _period_start(365))
        .scalar()
        or 0
    )

    total_screenings = db.query(func.count(ScreeningRecord.id)).scalar() or 0
    average_match_score = db.query(func.avg(ScreeningRecord.average_score)).scalar()

    return {
        "total_resumes": total_resumes,
        "resumes_today": resumes_today,
        "resumes_this_week": resumes_this_week,
        "resumes_this_month": resumes_this_month,
        "resumes_this_year": resumes_this_year,
        "total_screenings": total_screenings,
        "average_match_score": round(average_match_score, 2) if average_match_score else 0.0,
    }


def get_screening_activity(db: Session, days: int = 30) -> list[dict]:

    since = _period_start(days)
    rows = (
        db.query(
            func.date(ScreeningRecord.created_at).label("day"),
            func.count(ScreeningRecord.id).label("count"),
        )
        .filter(ScreeningRecord.created_at >= since)
        .group_by("day")
        .order_by("day")
        .all()
    )
    return [{"date": row.day, "count": row.count} for row in rows]