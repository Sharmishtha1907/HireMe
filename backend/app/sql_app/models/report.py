from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.sql_app.base import Base


class Report(Base):
    __tablename__ = "interview_reports"

    id: Mapped[int] = mapped_column(primary_key=True)

    interview_id: Mapped[int] = mapped_column(
        ForeignKey("interviews.id"),
        unique=True,
        nullable=False,
    )

    overall_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    technical_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    communication_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    strengths: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    weaknesses: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    recommendation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    interview = relationship(
        "Interview",
        back_populates="report",
    )