from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from backend.app.schemas.common import MessageRoleEnum


class MessageCreate(BaseModel):
    id: Optional[str] = None
    role: MessageRoleEnum = MessageRoleEnum.USER
    content: str
    attachments: List[Dict[str, Any]] = Field(default_factory=list)
    explanation_document_id: Optional[str] = None


class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    attachments: List[Dict[str, Any]]
    explanation_document_id: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
