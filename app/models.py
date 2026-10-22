
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class JobApplication(Base):
    __tablename__ = "job_applications"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    company_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    job_role: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="Applied",
    )
    applied_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        default=date.today,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
