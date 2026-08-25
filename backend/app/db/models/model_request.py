from typing import Any, Dict, Optional
from sqlalchemy import ForeignKey, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base, TimestampMixin


class ModelRequestModel(Base, TimestampMixin):
    __tablename__ = "model_requests"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # request_id
    session_id: Mapped[Optional[str]] = mapped_column(
        String(64),
        ForeignKey("sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    model: Mapped[str] = mapped_column(String(128), nullable=False)
    request_type: Mapped[str] = mapped_column(String(64), nullable=False)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    token_usage: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)  # 'success', 'error'
    error_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    # Relationships
    session: Mapped[Optional["SessionModel"]] = relationship(  # noqa: F821
        "SessionModel",
        back_populates="model_requests",
    )
