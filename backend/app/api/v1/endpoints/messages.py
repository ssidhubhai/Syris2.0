from typing import List, Optional
from fastapi import APIRouter, Depends, Header, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.session import get_db
from backend.app.schemas.message import MessageCreate, MessageResponse
from backend.app.services.idempotency_service import IdempotencyService
from backend.app.services.message_service import MessageService

router = APIRouter()


@router.post(
    "/sessions/{id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Append a new message to a session",
)
async def create_message(
    id: str,
    payload: MessageCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    x_idempotency_key: Optional[str] = Header(None, alias="X-Idempotency-Key"),
):
    endpoint = f"/api/v1/sessions/{id}/messages"
    request_id = getattr(request.state, "request_id", "unknown-req")

    if x_idempotency_key:
        cached = await IdempotencyService.get_replayable_response(
            db=db,
            idempotency_key=x_idempotency_key,
            endpoint=endpoint,
            payload=payload.model_dump(mode="json"),
        )
        if cached:
            status_code, content = cached
            return JSONResponse(
                status_code=status_code,
                content=content,
                headers={"X-Cache-Lookup": "HIT"},
            )

    message = await MessageService.create_message(
        db=db,
        session_id=id,
        data=payload,
    )
    response_data = MessageResponse.model_validate(message).model_dump(mode="json")

    if x_idempotency_key:
        await IdempotencyService.store_response(
            db=db,
            idempotency_key=x_idempotency_key,
            request_id=request_id,
            endpoint=endpoint,
            payload=payload.model_dump(mode="json"),
            response_code=status.HTTP_201_CREATED,
            response_json=response_data,
        )

    return response_data


@router.get(
    "/sessions/{id}/messages",
    response_model=List[MessageResponse],
    summary="List all messages in a session",
)
async def list_messages(
    id: str,
    db: AsyncSession = Depends(get_db),
):
    messages = await MessageService.list_messages(db=db, session_id=id)
    return [MessageResponse.model_validate(m) for m in messages]
