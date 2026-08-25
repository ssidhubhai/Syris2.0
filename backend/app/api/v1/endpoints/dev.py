import logging
import uuid
from typing import Optional
from fastapi import APIRouter, Header, Request, status

from backend.app.providers.base import (
    ProviderInvalidPayloadException,
    ProviderStructuredRequest,
)
from backend.app.providers.google_provider import GoogleProvider
from backend.app.schemas.dev import (
    GeminiSmokeRequest,
    GeminiSmokeResponse,
    GeminiSmokeResult,
)

logger = logging.getLogger("syris.dev")
router = APIRouter()

# Instantiate singleton GoogleProvider instance for development endpoints
dev_google_provider = GoogleProvider()


@router.post(
    "/gemini-smoke",
    response_model=GeminiSmokeResponse,
    status_code=status.HTTP_200_OK,
    summary="Development-only controlled end-to-end Gemini structured smoke test",
)
async def dev_gemini_smoke(
    payload: GeminiSmokeRequest,
    request: Request,
    x_request_id: Optional[str] = Header(None, alias="X-Request-ID"),
) -> GeminiSmokeResponse:
    """
    Controlled development-only endpoint executing a tiny structured Gemini call.
    Proves: FastAPI -> GoogleProvider -> Gemini API -> Pydantic Validation -> Normalized Response.
    Does NOT invoke Teacher Engine, ExplanationDocument, or normal student session routing.
    """
    # 1. Resolve request ID
    request_id = (
        x_request_id
        or getattr(request.state, "request_id", None)
        or f"smoke-{uuid.uuid4().hex[:12]}"
    )

    # 2. Validate prompt
    prompt = payload.prompt.strip() if payload.prompt else ""
    if not prompt:
        raise ProviderInvalidPayloadException(
            message="Prompt cannot be empty.",
            provider="google",
            status_code=400,
            model_id=payload.model_id,
        )

    model_id = payload.model_id or "gemini-3.5-flash-lite"

    # 3. Construct provider-neutral structured request
    structured_req = ProviderStructuredRequest(
        request_id=request_id,
        model_id=model_id,
        prompt=prompt,
        temperature=0.0,
        response_schema=GeminiSmokeResult,
    )

    logger.info(
        f"[DEV SMOKE] Executing structured test request_id={request_id} model={model_id}"
    )

    # 4. Execute via GoogleProvider (strictly isolated)
    provider_resp = await dev_google_provider.generate_structured(structured_req)

    # 5. Return normalized API response
    return GeminiSmokeResponse(
        request_id=provider_resp.request_id,
        provider=provider_resp.provider,
        model=provider_resp.model_id,
        latency_ms=provider_resp.latency_ms,
        token_usage=provider_resp.token_usage,
        result=provider_resp.structured_output,
    )
