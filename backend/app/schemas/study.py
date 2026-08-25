from typing import Optional
from pydantic import BaseModel, Field
from backend.app.schemas.explanation import ExplanationDocumentSchema


class StudyAskRequest(BaseModel):
    session_id: Optional[str] = Field(
        default=None,
        description="Optional existing session ID. If omitted, a new study session will be initialized.",
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="The student's text query or academic question.",
    )
    model_id: Optional[str] = Field(
        default=None,
        description="Optional model ID override (must be CERTIFIED_FOR_DEV in registry).",
    )


class StudyAskResponse(BaseModel):
    request_id: str = Field(
        ...,
        description="Unique request tracing ID.",
    )
    session_id: str = Field(
        ...,
        description="Associated active study session ID.",
    )
    explanation_document: ExplanationDocumentSchema = Field(
        ...,
        description="Validated ExplanationDocument rendered on the Digital Paper.",
    )
