import hashlib
import json
from typing import Any, Dict, Optional, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.errors import IdempotencyConflictException
from backend.app.db.models.idempotency import IdempotencyRecordModel


class IdempotencyService:
    @staticmethod
    def compute_request_hash(endpoint: str, payload: Any) -> str:
        """Computes deterministic SHA-256 hash of endpoint and payload."""
        serialized = json.dumps(payload, sort_keys=True, default=str)
        raw_str = f"{endpoint}:{serialized}"
        return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

    @staticmethod
    async def get_replayable_response(
        db: AsyncSession,
        idempotency_key: str,
        endpoint: str,
        payload: Any,
    ) -> Optional[Tuple[int, Dict[str, Any]]]:
        """
        Checks if an idempotency key has already been executed.
        - If matched with identical hash: returns (response_code, response_json)
        - If matched with different hash: raises IdempotencyConflictException
        - If not found: returns None
        """
        stmt = select(IdempotencyRecordModel).where(
            IdempotencyRecordModel.idempotency_key == idempotency_key
        )
        result = await db.execute(stmt)
        record = result.scalar_one_or_none()

        if not record:
            return None

        current_hash = IdempotencyService.compute_request_hash(endpoint, payload)
        if record.request_hash != current_hash:
            raise IdempotencyConflictException(
                key=idempotency_key,
                message="Idempotency key was previously used with a different request payload.",
            )

        return (record.response_code, record.response_json)

    @staticmethod
    async def store_response(
        db: AsyncSession,
        idempotency_key: str,
        request_id: str,
        endpoint: str,
        payload: Any,
        response_code: int,
        response_json: Dict[str, Any],
    ) -> IdempotencyRecordModel:
        """Stores the response of a newly executed idempotent mutation."""
        request_hash = IdempotencyService.compute_request_hash(endpoint, payload)
        record = IdempotencyRecordModel(
            idempotency_key=idempotency_key,
            request_id=request_id,
            endpoint=endpoint,
            request_hash=request_hash,
            response_code=response_code,
            response_json=response_json,
        )
        db.add(record)
        await db.flush()
        return record
