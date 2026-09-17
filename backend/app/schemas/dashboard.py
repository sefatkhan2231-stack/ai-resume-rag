from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_resumes: int
    resumes_today: int
    resumes_this_week: int
    resumes_this_month: int
    resumes_this_year: int
    total_screenings: int
    average_match_score: float


class ActivityPoint(BaseModel):
    date: str
    count: int


class ScreeningHistoryItem(BaseModel):
    id: int
    screening_type: str
    number_of_resumes: int
    average_score: float
    created_at: str