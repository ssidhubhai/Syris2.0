import os
import time
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import pytest

# Load environment variables for live test runs
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")


from google.genai import errors as genai_errors
from google.genai import types as genai_types

from backend.app.providers.base import (
    BaseModelProvider,
    ImageContent,
    ModelMetadata,
    ModelNotCertifiedException,
    ProviderAuthenticationException,
    ProviderErrorCode,
    ProviderException,
    ProviderHealthResult,
    ProviderInvalidPayloadException,
    ProviderMalformedOutputException,
    ProviderMessage,
    ProviderModelNotFoundException,
    ProviderRateLimitException,
    ProviderResponse,
    ProviderStructuredRequest,
    ProviderTextRequest,
    ProviderTokenUsage,
    ProviderUnavailableException,
)
from backend.app.providers.google_provider import GoogleProvider
from backend.app.providers.registry import (
    CERTIFIED_FOR_DEV,
    CERTIFIED_FOR_PROD,
    ModelRegistry,
    default_registry,
)


# ============================================================================
# Tiny Test Schema for Structured Output Smoke Tests
# ============================================================================

class TinyPhysicsAssertion(BaseModel):
    law_name: str = Field(description="Name of the physical law")
    formula_latex: str = Field(description="Formula in LaTeX format")
    is_valid_for_non_inertial_frame: bool = Field(description="Whether valid in accelerating frame")


# ============================================================================
# 1. Provider Construction & Registry Tests
# ============================================================================

def test_provider_construction_and_name():
    provider = GoogleProvider(api_key="test-api-key-12345")
    assert provider.provider_name == "google"
    assert isinstance(provider, BaseModelProvider)


def test_registry_certified_models():
    registry = ModelRegistry()
    certified_models = registry.list_models(provider="google", certified_only=True)
    model_ids = {m.model_id for m in certified_models}

    assert "gemini-3.5-flash-lite" in model_ids
    assert "gemini-3.5-flash" in model_ids
    assert "gemini-2.5-flash" in model_ids

    for m in certified_models:
        assert m.provider == "google"
        assert m.certification_status == CERTIFIED_FOR_DEV
        assert m.supports_structured_output is True
        assert m.supports_tools is True
        assert m.supports_streaming is True
        assert "text" in m.supported_modalities
        assert "image" in m.supported_modalities
        assert m.input_token_limit == 1048576
        assert m.output_token_limit == 65536
        assert m.last_verified_at is not None


def test_registry_validate_eligibility_pass():
    registry = ModelRegistry()
    meta = registry.validate_eligibility("gemini-3.5-flash-lite")
    assert meta.model_id == "gemini-3.5-flash-lite"
    assert meta.certification_status == CERTIFIED_FOR_DEV


def test_registry_validate_eligibility_unknown_model_rejection():
    registry = ModelRegistry()
    with pytest.raises(ModelNotCertifiedException) as exc_info:
        registry.validate_eligibility("gemini-1.5-flash")

    assert exc_info.value.error_code == ProviderErrorCode.MODEL_NOT_CERTIFIED
    assert exc_info.value.model_id == "gemini-1.5-flash"
    assert exc_info.value.is_transient is False


def test_registry_validate_eligibility_uncertified_model_rejection():
    registry = ModelRegistry()
    registry.register(
        ModelMetadata(
            provider="google",
            model_id="unapproved-experimental-model",
            api_version="v1",
            certification_status="UNCERTIFIED",
        )
    )
    with pytest.raises(ModelNotCertifiedException) as exc_info:
        registry.validate_eligibility("unapproved-experimental-model", required_status=CERTIFIED_FOR_DEV)

    assert exc_info.value.error_code == ProviderErrorCode.MODEL_NOT_CERTIFIED


# ============================================================================
# 2. Text Generation & Normalization Tests (Mocked)
# ============================================================================

@pytest.mark.asyncio
async def test_generate_text_success():
    # Setup mock client
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Newton's Second Law states that F = ma."
    mock_response.model_version = "gemini-3.5-flash-lite-001"
    mock_response.response_id = "resp-12345"
    
    mock_candidate = MagicMock()
    mock_candidate.finish_reason = "STOP"
    mock_response.candidates = [mock_candidate]

    mock_usage = MagicMock()
    mock_usage.prompt_token_count = 15
    mock_usage.candidates_token_count = 10
    mock_usage.total_token_count = 25
    mock_usage.cached_content_token_count = 0
    mock_response.usage_metadata = mock_usage

    mock_client.aio.models.generate_content = AsyncMock(return_value=mock_response)

    provider = GoogleProvider(client=mock_client)
    req = ProviderTextRequest(
        request_id="req-test-001",
        model_id="gemini-3.5-flash-lite",
        prompt="State Newton's Second Law.",
        temperature=0.2,
    )

    resp = await provider.generate_text(req)

    assert isinstance(resp, ProviderResponse)
    assert resp.request_id == "req-test-001"
    assert resp.provider == "google"
    assert resp.model_id == "gemini-3.5-flash-lite"
    assert resp.text == "Newton's Second Law states that F = ma."
    assert resp.token_usage.input_tokens == 15
    assert resp.token_usage.output_tokens == 10
    assert resp.token_usage.total_tokens == 25
    assert resp.token_usage.cached_tokens == 0
    assert resp.finish_reason == "STOP"
    assert resp.raw_metadata["model_version"] == "gemini-3.5-flash-lite-001"
    assert resp.latency_ms >= 0


@pytest.mark.asyncio
async def test_generate_text_fails_for_uncertified_model():
    mock_client = MagicMock()
    provider = GoogleProvider(client=mock_client)

    req = ProviderTextRequest(
        request_id="req-test-uncertified",
        model_id="gemini-2.0-flash",  # not certified in registry
        prompt="Explain momentum conservation.",
    )

    with pytest.raises(ModelNotCertifiedException) as exc_info:
        await provider.generate_text(req)

    assert exc_info.value.error_code == ProviderErrorCode.MODEL_NOT_CERTIFIED
    assert exc_info.value.model_id == "gemini-2.0-flash"


# ============================================================================
# 3. Structured Output Tests (Mocked)
# ============================================================================

@pytest.mark.asyncio
async def test_generate_structured_success():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '{"law_name": "Newton Second Law", "formula_latex": "F = m a", "is_valid_for_non_inertial_frame": false}'
    mock_response.model_version = "gemini-3.5-flash-001"
    mock_response.response_id = "resp-struct-001"

    mock_usage = MagicMock()
    mock_usage.prompt_token_count = 20
    mock_usage.candidates_token_count = 18
    mock_usage.total_token_count = 38
    mock_usage.cached_content_token_count = None
    mock_response.usage_metadata = mock_usage
    mock_response.candidates = []

    mock_client.aio.models.generate_content = AsyncMock(return_value=mock_response)

    provider = GoogleProvider(client=mock_client)
    req = ProviderStructuredRequest(
        request_id="req-struct-001",
        model_id="gemini-3.5-flash",
        prompt="Return the law definition in structured JSON.",
        response_schema=TinyPhysicsAssertion,
    )

    resp = await provider.generate_structured(req)

    assert isinstance(resp, ProviderResponse)
    assert resp.request_id == "req-struct-001"
    assert resp.provider == "google"
    assert isinstance(resp.structured_output, TinyPhysicsAssertion)
    assert resp.structured_output.law_name == "Newton Second Law"
    assert resp.structured_output.formula_latex == "F = m a"
    assert resp.structured_output.is_valid_for_non_inertial_frame is False
    assert resp.token_usage.total_tokens == 38


@pytest.mark.asyncio
async def test_generate_structured_rejects_malformed_json():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = 'NOT_A_VALID_JSON_STRING'
    mock_response.usage_metadata = None
    mock_response.candidates = []

    mock_client.aio.models.generate_content = AsyncMock(return_value=mock_response)

    provider = GoogleProvider(client=mock_client)
    req = ProviderStructuredRequest(
        request_id="req-struct-bad-json",
        model_id="gemini-3.5-flash-lite",
        prompt="Return structured JSON.",
        response_schema=TinyPhysicsAssertion,
    )

    with pytest.raises(ProviderMalformedOutputException) as exc_info:
        await provider.generate_structured(req)

    assert exc_info.value.error_code == ProviderErrorCode.MALFORMED_OUTPUT
    assert exc_info.value.is_transient is False
    assert "raw_output_snippet" in exc_info.value.details


@pytest.mark.asyncio
async def test_generate_structured_rejects_schema_mismatch():
    mock_client = MagicMock()
    mock_response = MagicMock()
    # Missing required formula_latex and is_valid_for_non_inertial_frame fields
    mock_response.text = '{"law_name": "Incomplete Law"}'
    mock_response.usage_metadata = None
    mock_response.candidates = []

    mock_client.aio.models.generate_content = AsyncMock(return_value=mock_response)

    provider = GoogleProvider(client=mock_client)
    req = ProviderStructuredRequest(
        request_id="req-struct-mismatch",
        model_id="gemini-3.5-flash-lite",
        prompt="Return structured JSON.",
        response_schema=TinyPhysicsAssertion,
    )

    with pytest.raises(ProviderMalformedOutputException) as exc_info:
        await provider.generate_structured(req)

    assert exc_info.value.error_code == ProviderErrorCode.MALFORMED_OUTPUT
    assert "validation_error" in exc_info.value.details


# ============================================================================
# 4. Multimodal Support Tests (Mocked)
# ============================================================================

@pytest.mark.asyncio
async def test_multimodal_request_mapping():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "The diagram shows a block on an inclined plane of angle theta."
    mock_response.usage_metadata = None
    mock_response.candidates = []

    mock_client.aio.models.generate_content = AsyncMock(return_value=mock_response)

    provider = GoogleProvider(client=mock_client)

    fake_png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
    img = ImageContent(data=fake_png_bytes, mime_type="image/png")

    req = ProviderTextRequest(
        request_id="req-multimodal-001",
        model_id="gemini-3.5-flash-lite",
        prompt="Describe the forces shown in this diagram.",
        images=[img],
    )

    resp = await provider.generate_text(req)

    assert resp.text == "The diagram shows a block on an inclined plane of angle theta."
    
    # Verify generate_content received types.Part and prompt string
    call_args = mock_client.aio.models.generate_content.call_args
    assert call_args is not None
    contents = call_args.kwargs["contents"]
    assert len(contents) == 2
    assert isinstance(contents[0], genai_types.Part)
    assert contents[0].inline_data.mime_type == "image/png"
    assert contents[1] == "Describe the forces shown in this diagram."


def test_multimodal_empty_image_rejected():
    img = ImageContent(data=b"", mime_type="image/png")
    with pytest.raises(ProviderInvalidPayloadException) as exc_info:
        img.validate_content()
    assert exc_info.value.error_code == ProviderErrorCode.INVALID_PAYLOAD


def test_multimodal_unsupported_mime_type_rejected():
    img = ImageContent(data=b"dummy-data", mime_type="image/bmp")
    with pytest.raises(ProviderInvalidPayloadException) as exc_info:
        img.validate_content()
    assert exc_info.value.error_code == ProviderErrorCode.INVALID_PAYLOAD
    assert "Unsupported image MIME type" in exc_info.value.message


# ============================================================================
# 5. Token Usage Normalization Tests
# ============================================================================

def test_token_usage_normalization_full():
    provider = GoogleProvider(api_key="test")
    usage_mock = MagicMock()
    usage_mock.prompt_token_count = 100
    usage_mock.candidates_token_count = 50
    usage_mock.total_token_count = 150
    usage_mock.cached_content_token_count = 20

    normalized = provider._normalize_token_usage(usage_mock)
    assert normalized.input_tokens == 100
    assert normalized.output_tokens == 50
    assert normalized.total_tokens == 150
    assert normalized.cached_tokens == 20


def test_token_usage_normalization_none_never_fabricates():
    provider = GoogleProvider(api_key="test")
    normalized = provider._normalize_token_usage(None)
    assert normalized.input_tokens == 0
    assert normalized.output_tokens == 0
    assert normalized.total_tokens == 0
    assert normalized.cached_tokens is None


# ============================================================================
# 6. Error Normalization Table Tests
# ============================================================================

@pytest.mark.parametrize(
    "status_code,expected_exception,expected_error_code,expected_transient",
    [
        (503, ProviderUnavailableException, ProviderErrorCode.PROVIDER_UNAVAILABLE, True),
        (429, ProviderRateLimitException, ProviderErrorCode.RATE_LIMIT_EXCEEDED, True),
        (400, ProviderInvalidPayloadException, ProviderErrorCode.INVALID_PAYLOAD, False),
        (401, ProviderAuthenticationException, ProviderErrorCode.AUTH_FAILURE, False),
        (403, ProviderAuthenticationException, ProviderErrorCode.AUTH_FAILURE, False),
        (404, ProviderModelNotFoundException, ProviderErrorCode.MODEL_NOT_FOUND, False),
    ],
)
def test_error_normalization_status_codes(status_code, expected_exception, expected_error_code, expected_transient):
    provider = GoogleProvider(api_key="test")
    api_err = genai_errors.APIError(status_code, f"Mock error message for {status_code}")
    
    normalized = provider._normalize_error(api_err, model_id="gemini-3.5-flash-lite")

    assert isinstance(normalized, expected_exception)
    assert normalized.error_code == expected_error_code
    assert normalized.status_code == status_code
    assert normalized.is_transient == expected_transient
    assert normalized.provider == "google"
    assert normalized.model_id == "gemini-3.5-flash-lite"


def test_error_normalization_transient_connection_timeout():
    provider = GoogleProvider(api_key="test")
    timeout_err = TimeoutError("Connection timed out after 30s")
    
    normalized = provider._normalize_error(timeout_err, model_id="gemini-3.5-flash-lite")

    assert isinstance(normalized, ProviderUnavailableException)
    assert normalized.error_code == ProviderErrorCode.PROVIDER_UNAVAILABLE
    assert normalized.is_transient is True


# ============================================================================
# 7. Lightweight Health Check Tests
# ============================================================================

@pytest.mark.asyncio
async def test_health_check_healthy():
    mock_client = MagicMock()
    mock_model = MagicMock()
    mock_model.name = "models/gemini-3.5-flash-lite"
    mock_client.aio.models.get = AsyncMock(return_value=mock_model)

    provider = GoogleProvider(client=mock_client)
    res = await provider.health_check()

    assert isinstance(res, ProviderHealthResult)
    assert res.provider == "google"
    assert res.is_healthy is True
    assert res.details["status"] == "connected"
    assert res.latency_ms >= 0


@pytest.mark.asyncio
async def test_health_check_auth_failure():
    mock_client = MagicMock()
    mock_client.aio.models.get = AsyncMock(
        side_effect=genai_errors.APIError(401, "API key not valid. Please pass a valid API key.")
    )

    provider = GoogleProvider(client=mock_client)
    res = await provider.health_check()

    assert isinstance(res, ProviderHealthResult)
    assert res.provider == "google"
    assert res.is_healthy is False
    assert res.details["error_code"] == ProviderErrorCode.AUTH_FAILURE.value
    assert res.details["is_transient"] is False
    assert "API key not valid" in (res.error_message or "")


# ============================================================================
# 8. Live Gemini API Test (Opt-in via RUN_LIVE_GEMINI_TESTS=1)
# ============================================================================

@pytest.mark.skipif(
    os.environ.get("RUN_LIVE_GEMINI_TESTS") != "1",
    reason="Live Gemini API tests disabled by default. Set RUN_LIVE_GEMINI_TESTS=1 to run.",
)
@pytest.mark.asyncio
async def test_live_gemini_provider_smoke():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    assert api_key, "GEMINI_API_KEY must be set when RUN_LIVE_GEMINI_TESTS=1"

    provider = GoogleProvider(api_key=api_key)

    # 1. Health check (0 tokens generated)
    health = await provider.health_check()
    assert health.is_healthy is True, f"Live health check failed: {health.error_message}"

    # 2. Text generation smoke test
    req = ProviderTextRequest(
        request_id="live-smoke-text-001",
        model_id="gemini-3.5-flash-lite",
        prompt="Say 'SYRIS_VERIFIED' in exactly one word.",
        temperature=0.0,
    )
    t0 = time.perf_counter()
    resp = await provider.generate_text(req)
    latency_ms = int((time.perf_counter() - t0) * 1000)

    assert resp.text is not None
    assert "SYRIS_VERIFIED" in resp.text
    assert resp.token_usage.input_tokens > 0
    assert resp.token_usage.output_tokens > 0
    print(
        f"\n[LIVE TEST RESULT] Model: gemini-3.5-flash-lite | Text Generation | Latency: {latency_ms}ms | "
        f"Usage: {resp.token_usage.total_tokens} tokens"
    )

    # 3. Structured output smoke test
    struct_req = ProviderStructuredRequest(
        request_id="live-smoke-struct-001",
        model_id="gemini-3.5-flash-lite",
        prompt="State Newton's Second Law in LaTeX and specify if it applies directly to non-inertial frames without pseudo-force.",
        response_schema=TinyPhysicsAssertion,
    )
    t1 = time.perf_counter()
    struct_resp = await provider.generate_structured(struct_req)
    latency_struct_ms = int((time.perf_counter() - t1) * 1000)

    assert isinstance(struct_resp.structured_output, TinyPhysicsAssertion)
    assert len(struct_resp.structured_output.law_name) > 0
    assert len(struct_resp.structured_output.formula_latex) > 0
    print(
        f"[LIVE TEST RESULT] Model: gemini-3.5-flash-lite | Structured Output | Latency: {latency_struct_ms}ms | "
        f"Parsed: {struct_resp.structured_output.law_name} ({struct_resp.structured_output.formula_latex})"
    )
