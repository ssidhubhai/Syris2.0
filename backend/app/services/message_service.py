import uuid
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.security import validate_identifier
from backend.app.db.models.message import MessageModel
from backend.app.db.models.session import SessionModel
from backend.app.db.base import utc_now
from backend.app.schemas.message import MessageCreate
from backend.app.services.session_service import SessionService


class MessageService:
    @staticmethod
    async def create_message(
        db: AsyncSession,
        session_id: str,
        data: MessageCreate,
    ) -> MessageModel:
        # Validate session existence
        session = await SessionService.get_session(db, session_id)
        
        msg_id = data.id or f"msg-{uuid.uuid4().hex[:12]}"
        validate_identifier(msg_id, "message_id")

        message = MessageModel(
            id=msg_id,
            session_id=session.id,
            role=data.role.value,
            content=data.content,
            attachments=data.attachments,
            explanation_document_id=data.explanation_document_id,
        )
        db.add(message)
        
        # Touch session updated_at
        session.updated_at = utc_now()
        await db.flush()
        return message

    @staticmethod
    async def list_messages(db: AsyncSession, session_id: str) -> List[MessageModel]:
        await SessionService.get_session(db, session_id)
        stmt = (
            select(MessageModel)
            .where(MessageModel.session_id == session_id)
            .order_by(MessageModel.created_at.asc())
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())
