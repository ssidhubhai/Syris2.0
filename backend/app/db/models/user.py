from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base, TimestampMixin, utc_now


class UserModel(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    preferences: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)

    # Relationships
    sessions: Mapped[List["SessionModel"]] = relationship(  # noqa: F821
        "SessionModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )
