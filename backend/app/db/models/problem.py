from typing import Any, Dict, List, Optional
from sqlalchemy import ForeignKey, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base, TimestampMixin


class ProblemModel(Base, TimestampMixin):
    __tablename__ = "problems"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_image: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    normalized_text: Mapped[str] = mapped_column(Text, nullable=False)
    subject: Mapped[str] = mapped_column(String(64), nullable=False)
    problem_metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)

    # Relationships
    session: Mapped["SessionModel"] = relationship("SessionModel", back_populates="problems")  # noqa: F821
    attempts: Mapped[List["AttemptModel"]] = relationship(  # noqa: F821
        "AttemptModel",
        back_populates="problem",
        cascade="all, delete-orphan",
    )
