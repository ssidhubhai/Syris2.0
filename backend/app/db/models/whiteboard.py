from typing import Any, Dict
from sqlalchemy import ForeignKey, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base, TimestampMixin


class WhiteboardStateModel(Base, TimestampMixin):
    __tablename__ = "whiteboard_states"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    explanation_document_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("explanation_documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    state_json: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Relationships
    explanation_document: Mapped["ExplanationDocumentModel"] = relationship(  # noqa: F821
        "ExplanationDocumentModel",
        back_populates="whiteboard_states",
    )
