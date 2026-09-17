from fastapi import APIRouter, UploadFile, File, HTTPException

from app.api.dependencies import SettingsDep, DbDep
from app.schemas.resume import ResumeUploadResponse
from app.schemas.candidate import (
    BatchUploadResponse,
    CandidateUploadResult,
    RankRequest,
    RankResponse,
)
from app.services.resume_service import process_resume, ResumeProcessingError
from app.services.ranking_service import rank_candidates

router = APIRouter(prefix="/resumes", tags=["resumes"])


def _validate_pdf(file: UploadFile) -> None:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail=f"'{file.filename}' is not a PDF.")


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(settings: SettingsDep, db: DbDep, file: UploadFile = File(...)):
    _validate_pdf(file)
    try:
        candidate = process_resume(file, settings, db)
    except ResumeProcessingError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return ResumeUploadResponse(
        resume_id=candidate.resume_id,
        candidate_id=candidate.candidate_id,
        filename=candidate.filename,
        chunks_indexed=candidate.chunks_indexed,
    )


@router.post("/batch-upload", response_model=BatchUploadResponse)
async def batch_upload_resumes(
    settings: SettingsDep, db: DbDep, files: list[UploadFile] = File(...)
):

    uploaded: list[CandidateUploadResult] = []

    for file in files:
        if file.content_type != "application/pdf":
            uploaded.append(
                CandidateUploadResult(filename=file.filename, success=False, error="Not a PDF.")
            )
            continue

        try:
            candidate = process_resume(file, settings, db)
        except ResumeProcessingError as exc:
            uploaded.append(
                CandidateUploadResult(filename=file.filename, success=False, error=str(exc))
            )
            continue

        uploaded.append(
            CandidateUploadResult(
                filename=candidate.filename,
                success=True,
                candidate_id=candidate.candidate_id,
                resume_id=candidate.resume_id,
                chunks_indexed=candidate.chunks_indexed,
            )
        )

    return BatchUploadResponse(uploaded=uploaded)


@router.post("/rank", response_model=RankResponse)
def rank_resumes(payload: RankRequest, db: DbDep):

    result = rank_candidates(payload.job_description, db, candidate_ids=payload.candidate_ids)
    if not result["results"]:
        raise HTTPException(status_code=404, detail="No candidates found to rank. Upload resumes first.")
    return result