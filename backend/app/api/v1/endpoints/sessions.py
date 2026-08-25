from typing import List, Optional
from fastapi import APIRouter, Depends, Header, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.session import get_db
from backend.app.schemas.session import (
    SessionCreate,
    SessionDetailResponse,
    SessionResponse,
    SessionUpdate,
)
from backend.app.services.idempotency_service import IdempotencyService
from backend.app.services.session_service import SessionService

router = APIRouter()


@router.post(
    "/sessions",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new study session",
)
async def create_session(
    payload: SessionCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    x_idempotency_key: Optional[str] = Header(None, alias="X-Idempotency-Key"),
):
    endpoint = "/api/v1/sessions"
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

    session = await SessionService.create_session(db=db, data=payload)
    response_data = SessionResponse.model_validate(session).model_dump(mode="json")

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
    "/sessions",
    response_model=List[SessionResponse],
    summary="List recent study sessions",
)
async def list_sessions(
    user_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    sessions = await SessionService.list_sessions(
        db=db, user_id=user_id, limit=limit, offset=offset
    )
    return [SessionResponse.model_validate(s) for s in sessions]


@router.get(
    "/sessions/{id}",
    response_model=SessionDetailResponse,
    summary="Get full session detail and history",
)
async def get_session(
    id: str,
    db: AsyncSession = Depends(get_db),
):
    return await SessionService.get_session_detail(db=db, session_id=id)


@router.patch(
    "/sessions/{id}",
    response_model=SessionResponse,
    summary="Update session title, subject or state",
)
async def update_session(
    id: str,
    payload: SessionUpdate,
    db: AsyncSession = Depends(get_db),
):
    session = await SessionService.update_session(db=db, session_id=id, update_data=payload)
    return SessionResponse.model_validate(session)
