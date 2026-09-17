from pydantic import BaseModel

class ResumeUploadResponse(BaseModel):
    resume_id: str
    candidate_id: str
    filename: str
    chunks_indexed: int