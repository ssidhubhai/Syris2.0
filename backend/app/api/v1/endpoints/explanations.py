from typing import Optional
from fastapi import APIRouter, Depends, Header, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.session import get_db
from backend.app.schemas.explanation import (
    ExplanationDocumentResponse,
    ExplanationDocumentSchema,
)
from backend.app.services.explanation_service import ExplanationService
from backend.app.services.idempotency_service import IdempotencyService

router = APIRouter()


@router.post(
    "/sessions/{id}/explanations",
    response_model=ExplanationDocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Persist a canonical ExplanationDocument into a session",
)
async def create_explanation(
    id: str,
    payload: ExplanationDocumentSchema,
    request: Request,
    db: AsyncSession = Depends(get_db),
    x_idempotency_key: Optional[str] = Header(None, alias="X-Idempotency-Key"),
):
    endpoint = f"/api/v1/sessions/{id}/explanations"
    request_id = getattr(request.state, "request_id", "unknown-req")

    if x_idempotency_key:
        cached = await IdempotencyService.get_replayable_response(
            db=db,
            idempotency_key=x_idempotency_key,
            endpoint=endpoint,
            payload=payload.model_dump(mode="json", by_alias=True),
        )
        if cached:
            status_code, content = cached
            return JSONResponse(
                status_code=status_code,
                content=content,
                headers={"X-Cache-Lookup": "HIT"},
            )

    doc_model = await ExplanationService.create_explanation(
        db=db,
        session_id=id,
        data=payload,
    )
    response_data = ExplanationDocumentResponse.model_validate(doc_model).model_dump(mode="json")

    if x_idempotency_key:
        await IdempotencyService.store_response(
            db=db,
            idempotency_key=x_idempotency_key,
            request_id=request_id,
            endpoint=endpoint,
            payload=payload.model_dump(mode="json", by_alias=True),
            response_code=status.HTTP_201_CREATED,
            response_json=response_data,
        )

    return response_data


@router.get(
    "/sessions/{id}/explanations/latest",
    response_model=ExplanationDocumentResponse,
    summary="Retrieve the latest ExplanationDocument for a session",
)
async def get_latest_explanation(
    id: str,
    db: AsyncSession = Depends(get_db),
):
    doc_model = await ExplanationService.get_latest_explanation_for_session(
        db=db, session_id=id
    )
    return ExplanationDocumentResponse.model_validate(doc_model)


@router.get(
    "/sessions/{id}/explanations/{doc_id}",
    response_model=ExplanationDocumentResponse,
    summary="Retrieve a specific ExplanationDocument by ID",
)
async def get_explanation_by_id(
    id: str,
    doc_id: str,
    db: AsyncSession = Depends(get_db),
):
    doc_model = await ExplanationService.get_explanation(
        db=db, document_id=doc_id
    )
    return ExplanationDocumentResponse.model_validate(doc_model)
