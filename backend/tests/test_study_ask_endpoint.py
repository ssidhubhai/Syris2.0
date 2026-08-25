import os
import time
from pathlib import Path
from unittest.mock import AsyncMock, patch
from dotenv import load_dotenv
import pytest
from httpx import AsyncClient

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

from backend.app.api.v1.endpoints.study import study_explanation_generator
from backend.app.ai.validation import SemanticValidationException
from backend.app.providers.base import (
    ProviderErrorCode,
    ProviderRateLimitException,
    ProviderResponse,
    ProviderTokenUsage,
    ProviderUnavailableException,
)
from backend.app.schemas.explanation import (
    ExplanationDocumentSchema,
    ExplanationNodeSchema,
    RelationshipSchema,
)


def _build_mock_friction_doc(session_id: str = "sess-123") -> ExplanationDocumentSchema:
    return ExplanationDocumentSchema(
        document_id="doc-friction-001",
        session_id=session_id,
        title="Microscopic Origin of Friction",
        intent="concept_explanation",
        subject="physics",
        language="english",
        nodes=[
            ExplanationNodeSchema(
                id="node-head-1",
                type="heading",
                content={"text": "Why Friction Opposes Relative Motion", "level": 1},
            ),
            ExplanationNodeSchema(
                id="node-text-1",
                type="text",
                content={
                    "markdown": "At the microscopic level, contact surfaces have irregularities (asperities). When two surfaces slide past each other, adhesive cold welds and interlocking asperities generate electromagnetic resistive forces opposing the direction of relative slip."
                },
            ),
            ExplanationNodeSchema(
                id="node-def-1",
                type="definition",
                content={
                    "title": "Coulomb's Law of Friction",
                    "latex": "f_k = \\mu_k N",
                    "annotation": "Kinetic friction opposes the instantaneous relative velocity vector.",
                },
            ),
        ],
        relationships=[
            RelationshipSchema(
                from_node="node-head-1",
                to_node="node-text-1",
                type="explains",
            ),
            RelationshipSchema(
                from_node="node-text-1",
                to_node="node-def-1",
                type="defines",
            ),
        ],
    )


# ============================================================================
# 1. Mocked Unit Tests for /api/v1/study/ask
# ============================================================================

@pytest.mark.asyncio
async def test_study_ask_creates_session_and_persists_explanation(client: AsyncClient):
    mock_doc = _build_mock_friction_doc()
    mock_provider_resp = ProviderResponse(
        request_id="req-study-001",
        provider="google",
        model_id="gemini-3.5-flash-lite",
        text=None,
        structured_output=mock_doc,
        token_usage=ProviderTokenUsage(input_tokens=150, output_tokens=220, total_tokens=370),
        latency_ms=750,
    )

    with patch.object(
        study_explanation_generator,
        "generate_explanation",
        new=AsyncMock(return_value=(mock_doc, mock_provider_resp)),
    ):
        response = await client.post(
            "/api/v1/study/ask",
            json={"message": "Why does friction oppose the tendency of relative motion?"},
            headers={"X-Request-ID": "req-study-001"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["request_id"] == "req-study-001"
    assert "session_id" in data
    assert data["explanation_document"]["title"] == "Microscopic Origin of Friction"
    assert len(data["explanation_document"]["nodes"]) == 3
    assert data["explanation_document"]["validation"]["math_verified"] is False
    assert data["explanation_document"]["validation"]["domain_verified"] is False

    session_id = data["session_id"]

    # Verify persistence by fetching session details
    sess_detail = await client.get(f"/api/v1/sessions/{session_id}")
    assert sess_detail.status_code == 200
    detail_data = sess_detail.json()
    assert len(detail_data["messages"]) == 1
    assert detail_data["messages"][0]["content"] == "Why does friction oppose the tendency of relative motion?"
    assert detail_data["latest_explanation"] is not None
    assert detail_data["latest_explanation"]["title"] == "Microscopic Origin of Friction"


@pytest.mark.asyncio
async def test_study_ask_with_existing_session_id(client: AsyncClient):
    # 1. Create a session first
    create_resp = await client.post(
        "/api/v1/sessions",
        json={"title": "Existing Session", "subject": "physics"},
    )
    assert create_resp.status_code == 201
    existing_session_id = create_resp.json()["id"]

    mock_doc = _build_mock_friction_doc(session_id=existing_session_id)
    mock_provider_resp = ProviderResponse(
        request_id="req-existing-002",
        provider="google",
        model_id="gemini-3.5-flash-lite",
        text=None,
        structured_output=mock_doc,
        latency_ms=600,
    )

    with patch.object(
        study_explanation_generator,
        "generate_explanation",
        new=AsyncMock(return_value=(mock_doc, mock_provider_resp)),
    ):
        response = await client.post(
            "/api/v1/study/ask",
            json={
                "session_id": existing_session_id,
                "message": "Explain friction in this existing session",
            },
            headers={"X-Request-ID": "req-existing-002"},
        )

    assert response.status_code == 200
    assert response.json()["session_id"] == existing_session_id


@pytest.mark.asyncio
async def test_study_ask_empty_message_rejected(client: AsyncClient):
    response = await client.post(
        "/api/v1/study/ask",
        json={"message": "   "},
        headers={"X-Request-ID": "req-empty-ask"},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == ProviderErrorCode.INVALID_PAYLOAD.value
    assert data["request_id"] == "req-empty-ask"


@pytest.mark.asyncio
async def test_study_ask_semantic_validation_failure_handling(client: AsyncClient):
    with patch.object(
        study_explanation_generator,
        "generate_explanation",
        side_effect=SemanticValidationException(
            message="Relationship to-node 'node-ghost-404' does not exist (dangling reference)."
        ),
    ):
        response = await client.post(
            "/api/v1/study/ask",
            json={"message": "Trigger semantic validation error"},
            headers={"X-Request-ID": "req-val-fail"},
        )

    assert response.status_code == 502
    data = response.json()
    assert data["error"]["code"] == ProviderErrorCode.MALFORMED_OUTPUT.value
    assert "dangling reference" in data["error"]["message"]


@pytest.mark.asyncio
async def test_study_ask_provider_rate_limit_error(client: AsyncClient):
    with patch.object(
        study_explanation_generator,
        "generate_explanation",
        side_effect=ProviderRateLimitException(
            message="Quota exceeded for gemini-3.5-flash-lite",
            provider="google",
            status_code=429,
        ),
    ):
        response = await client.post(
            "/api/v1/study/ask",
            json={"message": "Rate limit test"},
        )
    assert response.status_code == 429
    data = response.json()
    assert data["error"]["code"] == ProviderErrorCode.RATE_LIMIT_EXCEEDED.value


# ============================================================================
# 2. Live End-to-End Test (Opt-in via RUN_LIVE_GEMINI_TESTS=1)
# ============================================================================

@pytest.mark.skipif(
    os.environ.get("RUN_LIVE_GEMINI_TESTS") != "1",
    reason="Live Gemini API tests disabled by default. Set RUN_LIVE_GEMINI_TESTS=1 to run.",
)
@pytest.mark.asyncio
async def test_live_study_ask_e2e(client: AsyncClient):
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    assert api_key, "GEMINI_API_KEY must be set when RUN_LIVE_GEMINI_TESTS=1"

    test_queries = [
        ("What is centripetal acceleration?", "physics", "COMPACT_EXPLANATION"),
        ("Why does friction oppose the tendency of relative motion?", "physics", "CONCEPT_CENTRIC"),
        ("What is the difference between SN1 and SN2?", "chemistry", "COMPARISON"),
    ]

    for question, expected_subject, expected_strategy in test_queries:
        t0 = time.perf_counter()
        response = await client.post(
            "/api/v1/study/ask",
            json={"message": question},
            headers={"X-Request-ID": f"live-study-{int(time.time())}"},
        )
        elapsed_ms = int((time.perf_counter() - t0) * 1000)

        assert response.status_code == 200, f"Live request failed: {response.text}"
        data = response.json()
        doc = data["explanation_document"]

        assert doc["subject"] == expected_subject
        assert len(doc["nodes"]) >= 2
        assert doc["validation"]["math_verified"] is False
        assert doc["validation"]["domain_verified"] is False

        print(
            f"\n[LIVE STUDY ASK RESULT]\n"
            f"  Question: {question}\n"
            f"  Subject: {doc['subject']}\n"
            f"  Title: {doc['title']}\n"
            f"  Nodes: {len(doc['nodes'])} ({[n['type'] for n in doc['nodes']]})\n"
            f"  Relationships: {len(doc['relationships'])}\n"
            f"  Latency: {doc['source_metadata']['generation_time_ms']} ms (roundtrip: {elapsed_ms} ms)\n"
            f"  Session ID: {data['session_id']}\n"
        )
