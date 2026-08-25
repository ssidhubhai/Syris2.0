from enum import Enum
from typing import Any, Optional, TypeVar
from pydantic import BaseModel, ConfigDict
from backend.app.core.errors import ErrorCode

T = TypeVar("T")


class SubjectEnum(str, Enum):
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    MATHEMATICS = "mathematics"
    GENERAL = "general"


class SessionStateEnum(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    ARCHIVED = "archived"


class MessageRoleEnum(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Any] = None


class ErrorResponseEnvelope(BaseModel):
    error: ErrorDetail
    request_id: Optional[str] = None

    model_config = ConfigDict(extra="ignore")
