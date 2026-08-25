from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base, TimestampMixin, utc_now


class SessionModel(Base, TimestampMixin):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[Optional[str]] = mapped_column(
        String(64),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(64), nullable=False, default="physics")
    current_state: Mapped[str] = mapped_column(String(64), nullable=False, default="active")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    # Relationships
    user: Mapped[Optional["UserModel"]] = relationship("UserModel", back_populates="sessions")  # noqa: F821
    messages: Mapped[List["MessageModel"]] = relationship(  # noqa: F821
        "MessageModel",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="MessageModel.created_at",
    )
    problems: Mapped[List["ProblemModel"]] = relationship(  # noqa: F821
        "ProblemModel",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    explanation_documents: Mapped[List["ExplanationDocumentModel"]] = relationship(  # noqa: F821
        "ExplanationDocumentModel",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="ExplanationDocumentModel.created_at",
    )
    mistakes: Mapped[List["MistakeModel"]] = relationship(  # noqa: F821
        "MistakeModel",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    model_requests: Mapped[List["ModelRequestModel"]] = relationship(  # noqa: F821
        "ModelRequestModel",
        back_populates="session",
    )
