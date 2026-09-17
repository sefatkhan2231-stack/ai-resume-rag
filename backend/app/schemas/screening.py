

from pydantic import BaseModel, Field


class ScreeningRequest(BaseModel):
    job_description: str = Field(..., min_length=1)
    candidate_name: str = "Candidate"
    candidate_id: str = Field(..., min_length=1)


class Evidence(BaseModel):
    skill: str
    text: str

class ScreeningResponse(BaseModel):
    candidate: str
    score: float
    skills: dict[str, bool]
    missing_skills: list[str]
    evidence: list[Evidence]
    overall_assessment: str
    final_recommendation: str