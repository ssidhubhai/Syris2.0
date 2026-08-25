from typing import Any, Dict, List, Optional
from sqlalchemy import ForeignKey, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base, TimestampMixin


class ExplanationDocumentModel(Base, TimestampMixin):
    __tablename__ = "explanation_documents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # matches document_id
    session_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(64), nullable=False)
    intent: Mapped[str] = mapped_column(String(64), nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    document_json: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    validation_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    provider_metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)

    # Relationships
    session: Mapped["SessionModel"] = relationship(  # noqa: F821
        "SessionModel",
        back_populates="explanation_documents",
    )
    whiteboard_states: Mapped[List["WhiteboardStateModel"]] = relationship(  # noqa: F821
        "WhiteboardStateModel",
        back_populates="explanation_document",
        cascade="all, delete-orphan",
    )
