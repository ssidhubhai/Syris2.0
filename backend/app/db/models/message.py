from typing import Any, Dict, List, Optional
from sqlalchemy import ForeignKey, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base, TimestampMixin


class MessageModel(Base, TimestampMixin):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[str] = mapped_column(String(32), nullable=False)  # 'user', 'assistant', 'system'
    content: Mapped[str] = mapped_column(Text, nullable=False)
    attachments: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    explanation_document_id: Mapped[Optional[str]] = mapped_column(
        String(64),
        ForeignKey("explanation_documents.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    session: Mapped["SessionModel"] = relationship("SessionModel", back_populates="messages")  # noqa: F821
    explanation_document: Mapped[Optional["ExplanationDocumentModel"]] = relationship(  # noqa: F821
        "ExplanationDocumentModel"
    )
