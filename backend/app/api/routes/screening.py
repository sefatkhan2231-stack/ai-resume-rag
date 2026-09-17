

from fastapi import APIRouter

from app.services.screening_service import screen_candidate
from app.schemas.screening import ScreeningResponse, ScreeningRequest


router = APIRouter(prefix="/screening", tags=["screening"])


@router.post("/analyze", response_model=ScreeningResponse)
def analyze_candidate(payload: ScreeningRequest):
    return screen_candidate(
        job_description=payload.job_description,
        candidate_name=payload.candidate_name,
        candidate_id=payload.candidate_id,
    )