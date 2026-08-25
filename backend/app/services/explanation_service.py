import uuid
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.errors import (
    AppException,
    ErrorCode,
    InvalidExplanationDocumentException,
    SessionNotFoundException,
)
from backend.app.core.security import validate_identifier
from backend.app.db.models.explanation import ExplanationDocumentModel
from backend.app.db.models.whiteboard import WhiteboardStateModel
from backend.app.db.models.session import SessionModel
from backend.app.db.base import utc_now
from backend.app.schemas.explanation import (
    ExplanationDocumentCreate,
    ExplanationDocumentSchema,
)
from backend.app.services.session_service import SessionService


class ExplanationService:
    @staticmethod
    async def create_explanation(
        db: AsyncSession,
        session_id: str,
        data: ExplanationDocumentSchema,
        version: int = 1,
    ) -> ExplanationDocumentModel:
        # Validate session existence
        session = await SessionService.get_session(db, session_id)

        document_id = data.document_id or f"doc-{uuid.uuid4().hex[:12]}"
        validate_identifier(document_id, "document_id")

        # Serialized dict representations
        doc_json = data.model_dump(by_alias=True)
        validation_json = data.validation.model_dump()
        source_meta_json = data.source_metadata.model_dump()

        exp_model = ExplanationDocumentModel(
            id=document_id,
            session_id=session.id,
            title=data.title,
            subject=data.subject,
            intent=data.intent,
            version=version,
            document_json=doc_json,
            validation_json=validation_json,
            provider_metadata=source_meta_json,
        )
        db.add(exp_model)

        # Check for diagram / visual nodes to generate persistent whiteboard state
        for node in data.nodes:
            if node.type == "diagram" and isinstance(node.content, dict):
                wb_id = f"wb-{node.id}-{uuid.uuid4().hex[:8]}"
                wb_model = WhiteboardStateModel(
                    id=wb_id,
                    explanation_document_id=document_id,
                    state_json=node.content,
                    version=1,
                )
                db.add(wb_model)

        session.updated_at = utc_now()
        await db.flush()
        return exp_model

    @staticmethod
    async def get_explanation(
        db: AsyncSession,
        document_id: str,
    ) -> ExplanationDocumentModel:
        validate_identifier(document_id, "document_id")
        stmt = select(ExplanationDocumentModel).where(
            ExplanationDocumentModel.id == document_id
        )
        result = await db.execute(stmt)
        doc = result.scalar_one_or_none()
        if not doc:
            raise AppException(
                status_code=404,
                code="EXPLANATION_NOT_FOUND",
                message=f"Explanation document '{document_id}' was not found.",
                details={"document_id": document_id},
            )
        return doc

    @staticmethod
    async def get_latest_explanation_for_session(
        db: AsyncSession,
        session_id: str,
    ) -> ExplanationDocumentModel:
        await SessionService.get_session(db, session_id)
        stmt = (
            select(ExplanationDocumentModel)
            .where(ExplanationDocumentModel.session_id == session_id)
            .order_by(ExplanationDocumentModel.created_at.desc())
            .limit(1)
        )
        result = await db.execute(stmt)
        doc = result.scalar_one_or_none()
        if not doc:
            raise AppException(
                status_code=404,
                code="EXPLANATION_NOT_FOUND",
                message=f"No explanation documents found for session '{session_id}'.",
                details={"session_id": session_id},
            )
        return doc
