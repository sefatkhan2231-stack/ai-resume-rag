from datetime import datetime, timezone

from sqlalchemy import String, Integer, Float, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ScreeningRecord(Base):

    __tablename__ = "screening_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    screening_type: Mapped[str] = mapped_column(String)
    number_of_resumes: Mapped[int] = mapped_column(Integer)
    job_description: Mapped[str] = mapped_column(Text)
    average_score: Mapped[float] = mapped_column(Float)

    results_json: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )