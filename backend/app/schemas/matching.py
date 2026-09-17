from pydantic import BaseModel, Field


class JobMatchingRequest(BaseModel):
    job_description: str = Field(..., min_length=1)
    candidate_ids: list[str] | None = None


class MatchEvidence(BaseModel):
    skill: str
    text: str


class JobMatchResult(BaseModel):
    rank: int
    candidate_id: str
    resume_id: str
    name: str
    email: str | None
    phone: str | None
    score: float
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    gaps: list[str]
    evidence: list[MatchEvidence]
    overall_assessment: str
    final_recommendation: str
    recommendation: str


class JobMatchingResponse(BaseModel):
    results: list[JobMatchResult]
    average_score: float
    screening_id: int | None