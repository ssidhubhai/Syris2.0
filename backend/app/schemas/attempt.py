from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict


class AttemptCreate(BaseModel):
    id: Optional[str] = None
    problem_id: str
    raw_input: str
    normalized_input: Optional[str] = None
    analysis: Optional[Dict[str, Any]] = None


class AttemptResponse(BaseModel):
    id: str
    problem_id: str
    raw_input: str
    normalized_input: Optional[str]
    analysis: Optional[Dict[str, Any]]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
