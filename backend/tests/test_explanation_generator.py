from unittest.mock import AsyncMock
import pytest
from backend.app.ai.explanation_generator import ExplanationGenerator
from backend.app.providers.base import (
    BaseModelProvider,
    ProviderResponse,
    ProviderTokenUsage,
)
from backend.app.schemas.explanation import (
    ExplanationDocumentSchema,
    ExplanationNodeSchema,
    RelationshipSchema,
)


@pytest.fixture
def mock_candidate_doc() -> ExplanationDocumentSchema:
    return ExplanationDocumentSchema(
        document_id="doc-gen-100",
        session_id="sess-temp",
        title="Centripetal Force Concept",
        intent="definition",
        subject="physics",
        language="english",
        nodes=[
            ExplanationNodeSchema(
                id="node-head-1",
                type="heading",
                content={"text": "Centripetal Force Concept", "level": 1},
            ),
            ExplanationNodeSchema(
                id="node-def-1",
                type="definition",
                content={"title": "Centripetal Force", "latex": "F_c = \\frac{m v^2}{r}"},
            ),
        ],
        relationships=[],
    )


@pytest.mark.asyncio
async def test_explanation_generator_single_stage_success(mock_candidate_doc):
    mock_provider = AsyncMock(spec=BaseModelProvider)
    mock_provider.provider_name = "google"
    mock_provider.generate_structured.return_value = ProviderResponse(
        request_id="req-test-gen-001",
        provider="google",
        model_id="gemini-3.5-flash-lite",
        text=None,
        structured_output=mock_candidate_doc,
        token_usage=ProviderTokenUsage(input_tokens=100, output_tokens=150, total_tokens=250),
        latency_ms=850,
    )

    generator = ExplanationGenerator(provider=mock_provider, default_model="gemini-3.5-flash-lite")
    doc, resp = await generator.generate_explanation(
        query="What is centripetal acceleration?",
        session_id="sess-real-001",
        request_id="req-test-gen-001",
    )

    # 1. Single model call verification
    assert mock_provider.generate_structured.call_count == 1

    # 2. Invariants verification
    assert doc.session_id == "sess-real-001"
    assert doc.validation.math_verified is False
    assert doc.validation.domain_verified is False
    assert doc.source_metadata.provider == "google"
    assert doc.source_metadata.model == "gemini-3.5-flash-lite"
    assert doc.source_metadata.generation_time_ms == 850
    assert len(doc.nodes) == 2
