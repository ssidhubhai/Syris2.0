from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict


class ModelRequestCreate(BaseModel):
    id: str  # request_id
    session_id: Optional[str] = None
    provider: str
    model: str
    request_type: str
    latency_ms: int = 0
    token_usage: Optional[Dict[str, Any]] = None
    status: str
    error_code: Optional[str] = None


class ModelRequestResponse(BaseModel):
    id: str
    session_id: Optional[str]
    provider: str
    model: str
    request_type: str
    latency_ms: int
    token_usage: Optional[Dict[str, Any]]
    status: str
    error_code: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
