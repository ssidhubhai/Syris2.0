from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field
from backend.app.schemas.common import SubjectEnum


class ProblemCreate(BaseModel):
    id: Optional[str] = None
    source_image: Optional[str] = None
    normalized_text: str
    subject: SubjectEnum = SubjectEnum.PHYSICS
    problem_metadata: Dict[str, Any] = Field(default_factory=dict)


class ProblemResponse(BaseModel):
    id: str
    session_id: str
    source_image: Optional[str]
    normalized_text: str
    subject: str
    problem_metadata: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
