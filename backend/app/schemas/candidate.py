from pydantic import BaseModel, Field


class CandidateUploadResult(BaseModel):
    filename: str
    success: bool
    candidate_id: str | None = None
    resume_id: str | None = None
    chunks_indexed: int | None = None
    error: str | None = None


class BatchUploadResponse(BaseModel):
    uploaded: list[CandidateUploadResult]


class RankRequest(BaseModel):
    job_description: str = Field(..., min_length=1)
    candidate_ids: list[str] | None = None


class RankedCandidate(BaseModel):
    rank: int
    candidate_id: str
    resume_id: str
    name: str
    email: str | None
    phone: str | None
    score: float
    matched_skills: list[str]
    missing_skills: list[str]
    recommendation: str


class RankResponse(BaseModel):
    results: list[RankedCandidate]
    average_score: float
    screening_id: int | None