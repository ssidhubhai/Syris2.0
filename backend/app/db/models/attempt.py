from typing import Any, Dict, Optional
from sqlalchemy import ForeignKey, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base, TimestampMixin


class AttemptModel(Base, TimestampMixin):
    __tablename__ = "attempts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    problem_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("problems.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    raw_input: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_input: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    analysis: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Relationships
    problem: Mapped["ProblemModel"] = relationship("ProblemModel", back_populates="attempts")  # noqa: F821
