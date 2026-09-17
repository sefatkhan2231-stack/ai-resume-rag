

from fastapi import APIRouter

from app.schemas.job import JobDescriptionRequest, JobRequirementsResponse
from app.services.screening_service import get_job_requirements


router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/analyze", response_model=JobRequirementsResponse)
def analyze_job(payload: JobDescriptionRequest):
    return get_job_requirements(payload.job_description)