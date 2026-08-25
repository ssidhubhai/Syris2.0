from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from backend.app.schemas.common import SessionStateEnum, SubjectEnum
from backend.app.schemas.message import MessageResponse
from backend.app.schemas.problem import ProblemCreate, ProblemResponse
from backend.app.schemas.explanation import ExplanationDocumentResponse
from backend.app.schemas.whiteboard import WhiteboardStateResponse


class SessionCreate(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    title: Optional[str] = "New Study Session"
    subject: SubjectEnum = SubjectEnum.PHYSICS
    initial_problem: Optional[ProblemCreate] = None


class SessionUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[SubjectEnum] = None
    current_state: Optional[SessionStateEnum] = None


class SessionResponse(BaseModel):
    id: str
    user_id: Optional[str]
    title: str
    subject: str
    current_state: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SessionDetailResponse(BaseModel):
    id: str
    user_id: Optional[str]
    title: str
    subject: str
    current_state: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = Field(default_factory=list)
    problems: List[ProblemResponse] = Field(default_factory=list)
    latest_explanation: Optional[ExplanationDocumentResponse] = None
    latest_whiteboard: Optional[WhiteboardStateResponse] = None

    model_config = ConfigDict(from_attributes=True)
