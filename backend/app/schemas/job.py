from pydantic import BaseModel, Field


class JobDescriptionRequest(BaseModel):
    job_description: str = Field(..., min_length=1)

class JobRequirementsResponse(BaseModel):
    requirements: dict
    flattened: list[str]