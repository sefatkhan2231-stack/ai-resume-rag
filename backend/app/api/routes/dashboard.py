from fastapi import APIRouter

from app.api.dependencies import DbDep
from app.schemas.dashboard import DashboardStats, ActivityPoint, ScreeningHistoryItem
from app.services.dashboard_service import get_dashboard_stats, get_screening_activity
from app.models.screening import ScreeningRecord

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
def dashboard_stats(db: DbDep):
    return get_dashboard_stats(db)


@router.get("/activity", response_model=list[ActivityPoint])
def dashboard_activity(db: DbDep, days: int = 30):
    return get_screening_activity(db, days=days)


@router.get("/history", response_model=list[ScreeningHistoryItem])
def screening_history(db: DbDep, limit: int = 50):
    records = (
        db.query(ScreeningRecord)
        .order_by(ScreeningRecord.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        ScreeningHistoryItem(
            id=r.id,
            screening_type=r.screening_type,
            number_of_resumes=r.number_of_resumes,
            average_score=r.average_score,
            created_at=r.created_at.isoformat(),
        )
        for r in records
    ]