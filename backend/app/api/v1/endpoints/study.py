import logging
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Header, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.ai.explanation_generator import ExplanationGenerator
from backend.app.ai.validation import SemanticValidationException
from backend.app.core.errors import AppException, ErrorCode
from backend.app.db.session import get_db
from backend.app.providers.base import ProviderErrorCode, ProviderException
from backend.app.schemas.message import MessageCreate, MessageRoleEnum
from backend.app.schemas.session import SessionCreate, SubjectEnum
from backend.app.schemas.study import StudyAskRequest, StudyAskResponse
from backend.app.services.explanation_service import ExplanationService
from backend.app.services.message_service import MessageService
from backend.app.services.session_service import SessionService

logger = logging.getLogger("syris.study")
router = APIRouter()

# Shared generator instance
study_explanation_generator = ExplanationGenerator()


@router.post(
    "/ask",
    response_model=StudyAskResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask a question and generate an adaptive ExplanationDocument",
)
async def study_ask(
    payload: StudyAskRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    x_request_id: Optional[str] = Header(None, alias="X-Request-ID"),
):
    request_id = x_request_id or getattr(request.state, "request_id", f"req-ask-{uuid.uuid4().hex[:8]}")

    # 1. Validate prompt
    prompt = payload.message.strip()
    if not prompt:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": {
                    "code": ProviderErrorCode.INVALID_PAYLOAD.value,
                    "message": "The question message cannot be empty or whitespace.",
                },
                "request_id": request_id,
            },
        )

    # 2. Retrieve or create study session
    session = None
    if payload.session_id:
        session = await SessionService.get_session(db, payload.session_id)
    else:
        # Create new session with initial title based on query
        title_snippet = prompt[:45] + ("..." if len(prompt) > 45 else "")
        session = await SessionService.create_session(
            db,
            SessionCreate(
                title=title_snippet,
                subject=SubjectEnum.PHYSICS,
            ),
        )

    # 3. Persist student question as user message
    await MessageService.create_message(
        db,
        session_id=session.id,
        data=MessageCreate(
            role=MessageRoleEnum.USER,
            content=prompt,
        ),
    )

    # 4. Generate ExplanationDocument via single structured AI call
    try:
        explanation_doc, provider_resp = await study_explanation_generator.generate_explanation(
            query=prompt,
            session_id=session.id,
            request_id=request_id,
            model_id=payload.model_id,
        )
    except SemanticValidationException as val_err:
        logger.error(f"[STUDY_ASK] Semantic validation error request_id={request_id}: {val_err.message}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={
                "error": {
                    "code": ProviderErrorCode.MALFORMED_OUTPUT.value,
                    "message": f"Generated ExplanationDocument failed semantic validation: {val_err.message}",
                    "details": val_err.details,
                },
                "request_id": request_id,
            },
        )
    except ProviderException as prov_err:
        logger.error(f"[STUDY_ASK] Provider error request_id={request_id}: {prov_err.message}")
        return JSONResponse(
            status_code=prov_err.status_code or status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": {
                    "code": prov_err.error_code.value,
                    "message": prov_err.message,
                    "details": prov_err.details,
                },
                "request_id": request_id,
            },
        )

    # 5. Persist valid ExplanationDocument to DB
    await ExplanationService.create_explanation(
        db=db,
        session_id=session.id,
        data=explanation_doc,
    )

    # Update session title/subject if more specific
    if explanation_doc.title and session.title == "New Study Session":
        session.title = explanation_doc.title
    if explanation_doc.subject in ("physics", "chemistry", "mathematics"):
        session.subject = explanation_doc.subject

    await db.flush()

    return StudyAskResponse(
        request_id=request_id,
        session_id=session.id,
        explanation_document=explanation_doc,
    )
