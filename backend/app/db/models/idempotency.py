from typing import Any, Dict
from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.db.base import Base, TimestampMixin


class IdempotencyRecordModel(Base, TimestampMixin):
    __tablename__ = "idempotency_records"

    idempotency_key: Mapped[str] = mapped_column(String(128), primary_key=True)
    request_id: Mapped[str] = mapped_column(String(64), nullable=False)
    endpoint: Mapped[str] = mapped_column(String(255), nullable=False)
    request_hash: Mapped[str] = mapped_column(String(64), nullable=False)  # SHA256 hex
    response_code: Mapped[int] = mapped_column(Integer, nullable=False)
    response_json: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
