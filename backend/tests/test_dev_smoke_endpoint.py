import os
import time
from pathlib import Path
from unittest.mock import AsyncMock, patch
from dotenv import load_dotenv
import pytest
from httpx import AsyncClient

# Load environment variables for live test runs
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

from backend.app.api.v1.endpoints.dev import dev_google_provider
from backend.app.providers.base import (
    ModelNotCertifiedException,
    ProviderAuthenticationException,
    ProviderErrorCode,
    ProviderMalformedOutputException,
    ProviderRateLimitException,
    ProviderResponse,
    ProviderTokenUsage,
    ProviderUnavailableException,
)
from backend.app.schemas.dev import GeminiSmokeResult


# ============================================================================
# 1. Mocked Unit Tests for /api/v1/dev/gemini-smoke
# ============================================================================

@pytest.mark.asyncio
async def test_dev_gemini_smoke_mocked_success(client: AsyncClient):
    mock_smoke_result = GeminiSmokeResult(
        answer="Friction arises due to microscopic electrostatic interactions and surface interlocking between contacting surfaces, opposing relative motion.",
        confidence="high",
    )
    mock_provider_resp = ProviderResponse(
        request_id="req-smoke-001",
        provider="google",
        model_id="gemini-3.5-flash-lite",
        text=None,
        structured_output=mock_smoke_result,
        token_usage=ProviderTokenUsage(
            input_tokens=30,
            output_tokens=25,
            total_tokens=55,
            cached_tokens=0,
        ),
        latency_ms=450,
        finish_reason="STOP",
    )

    with patch.object(
        dev_google_provider,
        "generate_structured",
        new=AsyncMock(return_value=mock_provider_resp),
    ):
        response = await client.post(
            "/api/v1/dev/gemini-smoke",
            json={
                "prompt": "Why does friction oppose relative motion?",
                "model_id": "gemini-3.5-flash-lite",
            },
            headers={"X-Request-ID": "req-smoke-001"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["request_id"] == "req-smoke-001"
    assert data["provider"] == "google"
    assert data["model"] == "gemini-3.5-flash-lite"
    assert data["latency_ms"] == 450
    assert data["token_usage"]["total_tokens"] == 55
    assert data["result"]["confidence"] == "high"
    assert "electrostatic" in data["result"]["answer"]


@pytest.mark.asyncio
async def test_dev_gemini_smoke_empty_prompt_rejected(client: AsyncClient):
    response = await client.post(
        "/api/v1/dev/gemini-smoke",
        json={"prompt": "   "},
        headers={"X-Request-ID": "req-empty-prompt"},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == ProviderErrorCode.INVALID_PAYLOAD.value
    assert data["request_id"] == "req-empty-prompt"


@pytest.mark.asyncio
async def test_dev_gemini_smoke_uncertified_model_rejected(client: AsyncClient):
    with patch.object(
        dev_google_provider,
        "generate_structured",
        side_effect=ModelNotCertifiedException(
            model_id="unapproved-model",
            provider="google",
        ),
    ):
        response = await client.post(
            "/api/v1/dev/gemini-smoke",
            json={
                "prompt": "Test prompt",
                "model_id": "unapproved-model",
            },
        )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == ProviderErrorCode.MODEL_NOT_CERTIFIED.value


@pytest.mark.asyncio
async def test_dev_gemini_smoke_rate_limit_normalization(client: AsyncClient):
    with patch.object(
        dev_google_provider,
        "generate_structured",
        side_effect=ProviderRateLimitException(
            message="Resource has been exhausted (e.g. check quota).",
            provider="google",
            status_code=429,
        ),
    ):
        response = await client.post(
            "/api/v1/dev/gemini-smoke",
            json={"prompt": "Test prompt"},
        )
    assert response.status_code == 429
    data = response.json()
    assert data["error"]["code"] == ProviderErrorCode.RATE_LIMIT_EXCEEDED.value


@pytest.mark.asyncio
async def test_dev_gemini_smoke_service_unavailable_normalization(client: AsyncClient):
    with patch.object(
        dev_google_provider,
        "generate_structured",
        side_effect=ProviderUnavailableException(
            message="Google Gemini backend is temporarily unavailable.",
            provider="google",
            status_code=503,
        ),
    ):
        response = await client.post(
            "/api/v1/dev/gemini-smoke",
            json={"prompt": "Test prompt"},
        )
    assert response.status_code == 503
    data = response.json()
    assert data["error"]["code"] == ProviderErrorCode.PROVIDER_UNAVAILABLE.value


@pytest.mark.asyncio
async def test_dev_gemini_smoke_malformed_output_normalization(client: AsyncClient):
    with patch.object(
        dev_google_provider,
        "generate_structured",
        side_effect=ProviderMalformedOutputException(
            message="Failed to validate structured JSON.",
            provider="google",
            raw_output="INVALID_RAW_JSON",
        ),
    ):
        response = await client.post(
            "/api/v1/dev/gemini-smoke",
            json={"prompt": "Test prompt"},
        )
    assert response.status_code == 502
    data = response.json()
    assert data["error"]["code"] == ProviderErrorCode.MALFORMED_OUTPUT.value


# ============================================================================
# 2. Regression Check: Session Endpoints Isolation
# ============================================================================

@pytest.mark.asyncio
async def test_session_endpoints_remain_isolated_from_provider(client: AsyncClient):
    with patch.object(
        dev_google_provider,
        "generate_structured",
        new=AsyncMock(),
    ) as mock_structured:
        # Create session
        sess_resp = await client.post("/api/v1/sessions", json={"title": "Isolation Test", "subject": "physics"})
        assert sess_resp.status_code == 201
        session_id = sess_resp.json()["id"]

        # Append message
        msg_resp = await client.post(
            f"/api/v1/sessions/{session_id}/messages",
            json={"role": "user", "content": "Hello Teacher"},
        )
        assert msg_resp.status_code == 201

        # Verify GoogleProvider was NEVER invoked
        mock_structured.assert_not_called()


# ============================================================================
# 3. Live End-to-End Smoke Test (Opt-in via RUN_LIVE_GEMINI_TESTS=1)
# ============================================================================

@pytest.mark.skipif(
    os.environ.get("RUN_LIVE_GEMINI_TESTS") != "1",
    reason="Live Gemini API tests disabled by default. Set RUN_LIVE_GEMINI_TESTS=1 to run.",
)
@pytest.mark.asyncio
async def test_live_dev_gemini_smoke_e2e(client: AsyncClient):
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    assert api_key, "GEMINI_API_KEY must be set when RUN_LIVE_GEMINI_TESTS=1"

    prompt = (
        "You are being tested as an educational AI system.\n"
        "Return a very short answer to:\n"
        "Why does friction oppose the tendency of relative motion?\n\n"
        "Return only the requested structured fields."
    )

    t0 = time.perf_counter()
    response = await client.post(
        "/api/v1/dev/gemini-smoke",
        json={
            "prompt": prompt,
            "model_id": "gemini-3.5-flash-lite",
        },
        headers={"X-Request-ID": "live-smoke-e2e-001"},
    )
    elapsed_ms = int((time.perf_counter() - t0) * 1000)

    assert response.status_code == 200, f"Live request failed: {response.text}"
    data = response.json()

    assert data["request_id"] == "live-smoke-e2e-001"
    assert data["provider"] == "google"
    assert data["model"] == "gemini-3.5-flash-lite"
    assert data["latency_ms"] > 0
    assert "answer" in data["result"]
    assert len(data["result"]["answer"]) > 10
    assert data["result"]["confidence"] in ("high", "medium", "low")

    token_usage_str = (
        f"{data['token_usage']['total_tokens']} tokens"
        if data.get("token_usage")
        else "N/A"
    )

    print(
        f"\n[LIVE E2E SMOKE RESULT]\n"
        f"  Endpoint: POST /api/v1/dev/gemini-smoke\n"
        f"  Status: {response.status_code} OK\n"
        f"  Model: {data['model']}\n"
        f"  Request ID: {data['request_id']}\n"
        f"  Latency: {data['latency_ms']} ms (client roundtrip: {elapsed_ms} ms)\n"
        f"  Tokens: {token_usage_str}\n"
        f"  Confidence: {data['result']['confidence']}\n"
        f"  Answer: {data['result']['answer']}\n"
    )
