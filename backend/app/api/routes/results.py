from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.api.dependencies import DbDep
from app.models.screening import ScreeningRecord
from app.services.export_service import build_export

router = APIRouter(prefix="/results", tags=["results"])


@router.get("/export/{screening_id}")
def export_results(screening_id: int, db: DbDep):

    record = db.query(ScreeningRecord).filter(ScreeningRecord.id == screening_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Screening record not found.")

    csv_text, filename = build_export(record)

    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )