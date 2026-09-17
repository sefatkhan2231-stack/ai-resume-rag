from fastapi import APIRouter, HTTPException

from app.api.dependencies import DbDep
from app.schemas.matching import JobMatchingRequest, JobMatchingResponse
from app.services.matching_service import analyze_job_matching

router = APIRouter(prefix="/job-matching", tags=["job-matching"])


@router.post("/analyze", response_model=JobMatchingResponse)
def analyze_candidates(payload: JobMatchingRequest, db: DbDep):
    result = analyze_job_matching(payload.job_description, db, candidate_ids=payload.candidate_ids)
    if not result["results"]:
        raise HTTPException(
            status_code=404, detail="No candidates found to analyze. Upload resumes first."
        )
    return result