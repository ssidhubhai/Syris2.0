from typing import Any, Dict
from sqlalchemy import ForeignKey, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base, TimestampMixin


class MistakeModel(Base, TimestampMixin):
    __tablename__ = "mistakes"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    concept: Mapped[str] = mapped_column(String(128), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    evidence: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)

    # Relationships
    session: Mapped["SessionModel"] = relationship("SessionModel", back_populates="mistakes")  # noqa: F821
