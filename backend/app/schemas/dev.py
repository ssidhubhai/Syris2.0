from typing import Literal, Optional
from pydantic import BaseModel, Field
from backend.app.providers.base import ProviderTokenUsage


class GeminiSmokeResult(BaseModel):
    """Tiny structured schema for the Phase 3C development smoke test."""
    answer: str = Field(description="Short pedagogical answer to the test question.")
    confidence: Literal["high", "medium", "low"] = Field(
        description="Confidence rating of the generated response."
    )


class GeminiSmokeRequest(BaseModel):
    """Request payload for the controlled development smoke endpoint."""
    prompt: Optional[str] = Field(
        default=(
            "You are being tested as an educational AI system.\n"
            "Return a very short answer to:\n"
            "Why does friction oppose the tendency of relative motion?\n\n"
            "Return only the requested structured fields."
        ),
        description="Prompt to test structured generation.",
    )
    model_id: Optional[str] = Field(
        default="gemini-3.5-flash-lite",
        description="Certified development candidate model ID to test.",
    )


class GeminiSmokeResponse(BaseModel):
    """Normalized API response envelope for the smoke test."""
    request_id: str
    provider: str
    model: str
    latency_ms: int
    token_usage: Optional[ProviderTokenUsage] = None
    result: GeminiSmokeResult
