import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.errors import SessionNotFoundException
from backend.app.core.security import validate_identifier
from backend.app.db.models.session import SessionModel
from backend.app.db.models.problem import ProblemModel
from backend.app.db.models.explanation import ExplanationDocumentModel
from backend.app.db.models.whiteboard import WhiteboardStateModel
from backend.app.schemas.session import (
    SessionCreate,
    SessionDetailResponse,
    SessionResponse,
    SessionUpdate,
)
from backend.app.schemas.message import MessageResponse
from backend.app.schemas.problem import ProblemResponse
from backend.app.schemas.explanation import ExplanationDocumentResponse
from backend.app.schemas.whiteboard import WhiteboardStateResponse


class SessionService:
    @staticmethod
    async def create_session(db: AsyncSession, data: SessionCreate) -> SessionModel:
        session_id = data.id or f"sess-{uuid.uuid4().hex[:12]}"
        validate_identifier(session_id, "session_id")
        
        session = SessionModel(
            id=session_id,
            user_id=data.user_id,
            title=data.title or "New Study Session",
            subject=data.subject.value,
            current_state="active",
        )
        db.add(session)
        await db.flush()

        if data.initial_problem:
            prob_id = data.initial_problem.id or f"prob-{uuid.uuid4().hex[:12]}"
            problem = ProblemModel(
                id=prob_id,
                session_id=session_id,
                source_image=data.initial_problem.source_image,
                normalized_text=data.initial_problem.normalized_text,
                subject=data.initial_problem.subject.value,
                problem_metadata=data.initial_problem.problem_metadata,
            )
            db.add(problem)
            await db.flush()

        return session

    @staticmethod
    async def get_session(db: AsyncSession, session_id: str) -> SessionModel:
        validate_identifier(session_id, "session_id")
        stmt = select(SessionModel).where(SessionModel.id == session_id)
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        if not session:
            raise SessionNotFoundException(session_id=session_id)
        return session

    @staticmethod
    async def get_session_detail(db: AsyncSession, session_id: str) -> SessionDetailResponse:
        validate_identifier(session_id, "session_id")
        stmt = (
            select(SessionModel)
            .where(SessionModel.id == session_id)
            .options(
                selectinload(SessionModel.messages),
                selectinload(SessionModel.problems),
                selectinload(SessionModel.explanation_documents).selectinload(
                    ExplanationDocumentModel.whiteboard_states
                ),
            )
        )
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        if not session:
            raise SessionNotFoundException(session_id=session_id)

        # Extract latest explanation document and its whiteboard state if any
        latest_explanation = None
        latest_whiteboard = None
        if session.explanation_documents:
            latest_exp_model = session.explanation_documents[-1]
            latest_explanation = ExplanationDocumentResponse.model_validate(latest_exp_model)
            if latest_exp_model.whiteboard_states:
                latest_wb_model = latest_exp_model.whiteboard_states[-1]
                latest_whiteboard = WhiteboardStateResponse.model_validate(latest_wb_model)

        return SessionDetailResponse(
            id=session.id,
            user_id=session.user_id,
            title=session.title,
            subject=session.subject,
            current_state=session.current_state,
            created_at=session.created_at,
            updated_at=session.updated_at,
            messages=[MessageResponse.model_validate(m) for m in session.messages],
            problems=[ProblemResponse.model_validate(p) for p in session.problems],
            latest_explanation=latest_explanation,
            latest_whiteboard=latest_whiteboard,
        )

    @staticmethod
    async def list_sessions(
        db: AsyncSession,
        user_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[SessionModel]:
        stmt = select(SessionModel).order_by(SessionModel.updated_at.desc()).limit(limit).offset(offset)
        if user_id:
            stmt = stmt.where(SessionModel.user_id == user_id)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def update_session(
        db: AsyncSession,
        session_id: str,
        update_data: SessionUpdate,
    ) -> SessionModel:
        session = await SessionService.get_session(db, session_id)
        if update_data.title is not None:
            session.title = update_data.title
        if update_data.subject is not None:
            session.subject = update_data.subject.value
        if update_data.current_state is not None:
            session.current_state = update_data.current_state.value
        await db.flush()
        return session
