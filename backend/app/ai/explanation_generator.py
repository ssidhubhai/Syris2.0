import logging
import uuid
from pathlib import Path
from typing import Optional, Tuple
from backend.app.ai.context_analyzer import AnalysisContext, ContextAnalyzer
from backend.app.ai.presentation_planner import PresentationPlan, PresentationPlanner
from backend.app.ai.validation import SemanticValidator
from backend.app.core.config import settings
from backend.app.providers.base import (
    BaseModelProvider,
    ProviderResponse,
    ProviderStructuredRequest,
)
from backend.app.providers.google_provider import GoogleProvider
from backend.app.schemas.ai_explanation import AIExplanationDocumentSchema
from backend.app.schemas.explanation import (
    ExplanationDocumentSchema,
    LayoutHintsSchema,
    SourceMetadataSchema,
    ValidationMetadataSchema,
)

logger = logging.getLogger("syris.ai.generator")

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


def load_versioned_prompt(filename: str = "explanation_generator_v1_0.md") -> Tuple[str, str]:
    """Loads system prompt and extracts version header if present."""
    prompt_path = PROMPTS_DIR / filename
    if not prompt_path.exists():
        # Fallback to explanation_generator.md
        prompt_path = PROMPTS_DIR / "explanation_generator.md"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found in {PROMPTS_DIR}")

    raw_text = prompt_path.read_text(encoding="utf-8").strip()
    version = "v1.0"

    # Extract YAML frontmatter if present
    if raw_text.startswith("---"):
        parts = raw_text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if line.startswith("version:"):
                    version = f"v{line.split(':', 1)[1].strip().strip('\"').strip('\'')}"
            raw_text = parts[2].strip()

    return raw_text, version


class ExplanationGenerator:
    """
    Coordinates single-stage structured generation of ExplanationDocuments.
    Combines deterministic query analysis with unified structured AI generation.
    """

    def __init__(
        self,
        provider: Optional[BaseModelProvider] = None,
        default_model: Optional[str] = None,
        prompt_file: str = "explanation_generator_v1_0.md",
    ):
        self._provider = provider or GoogleProvider()
        self._default_model = default_model or settings.DEFAULT_AI_MODEL
        self._system_prompt, self._prompt_version = load_versioned_prompt(prompt_file)

    @property
    def prompt_version(self) -> str:
        return self._prompt_version

    async def generate_explanation(
        self,
        query: str,
        session_id: str,
        request_id: str,
        model_id: Optional[str] = None,
        tracer: Optional[Any] = None,
    ) -> Tuple[ExplanationDocumentSchema, ProviderResponse]:
        """
        Executes single-stage structured generation:
        Query -> Context -> Presentation Plan -> Structured Gemini Call -> Validation.
        """
        target_model = model_id or self._default_model

        # 1. Deterministic Context & Presentation Planning (0 extra LLM calls)
        if tracer:
            tracer.start_stage("preprocessing")
        context: AnalysisContext = ContextAnalyzer.analyze(query)
        plan: PresentationPlan = PresentationPlanner.plan(context)
        if tracer:
            tracer.end_stage("preprocessing")


        logger.info(
            f"[AI_GENERATOR] Preparing generation request_id={request_id} "
            f"model={target_model} subject={context.subject} intent={context.intent} "
            f"strategy={plan.strategy}"
        )

        # 2. Build single-stage structured prompt
        if tracer:
            tracer.start_stage("prompt_prep")
        user_prompt = (
            f"Student Question: {query}\n\n"
            f"[Context Analysis]\n"
            f"- Subject: {context.subject}\n"
            f"- Intent: {context.intent}\n"
            f"- Complexity: {context.complexity}\n"
            f"- Language: {context.language}\n"
            f"- Presentation Strategy: {plan.strategy}\n"
            f"- Strategy Rationale: {plan.justification}\n\n"
            f"Generate a comprehensive, pedagogically sound ExplanationDocument matching this strategy. "
            f"Set document_id to a new unique ID (e.g. 'doc-{uuid.uuid4().hex[:8]}') and session_id to '{session_id}'."
        )

        structured_req = ProviderStructuredRequest(
            request_id=request_id,
            model_id=target_model,
            prompt=user_prompt,
            system_instruction=self._system_prompt,
            response_schema=AIExplanationDocumentSchema,
            temperature=0.2,
        )
        if tracer:
            tracer.end_stage("prompt_prep")

        # 3. Execute ONE structured AI model call
        if tracer:
            tracer.start_stage("gemini_request")
        provider_resp: ProviderResponse = await self._provider.generate_structured(structured_req)
        if tracer:
            tracer.end_stage("gemini_request")

        # 4. Parse response & convert to canonical ExplanationDocumentSchema
        if tracer:
            tracer.start_stage("response_parse")
        raw_doc = provider_resp.structured_output
        if isinstance(raw_doc, AIExplanationDocumentSchema):
            candidate_doc = ExplanationDocumentSchema.model_validate(raw_doc.model_dump(by_alias=True))
        elif isinstance(raw_doc, dict):
            candidate_doc = ExplanationDocumentSchema.model_validate(raw_doc)
        else:
            candidate_doc = raw_doc

        # Standardize metadata invariants
        if not candidate_doc.document_id:
            candidate_doc.document_id = f"doc-{uuid.uuid4().hex[:12]}"
        candidate_doc.session_id = session_id

        # Invariant: math_verified and domain_verified remain FALSE in Phase 4A/4B
        candidate_doc.validation = ValidationMetadataSchema(
            math_verified=False,
            domain_verified=False,
            verifier_used="semantic_validator_phase4a",
            flagged_issues=[],
        )

        candidate_doc.source_metadata = SourceMetadataSchema(
            provider=self._provider.provider_name,
            model=target_model,
            generation_time_ms=provider_resp.latency_ms,
        )
        # Record versioned prompt identifier in source metadata
        if hasattr(candidate_doc.source_metadata, "__dict__"):
            candidate_doc.source_metadata.prompt_version = self._prompt_version  # type: ignore[attr-defined]

        # Attach recommended layout hints if not provided by model
        if not candidate_doc.layout_hints:
            candidate_doc.layout_hints = LayoutHintsSchema(
                recommended_layout=plan.recommended_layout
            )
        if tracer:
            tracer.end_stage("response_parse")

        # 5. Strict Semantic Validation (fails closed on invalid IDs or dangling references)
        if tracer:
            tracer.start_stage("validation")
        SemanticValidator.validate(candidate_doc)
        if tracer:
            tracer.end_stage("validation")

        logger.info(
            f"[AI_GENERATOR] Generation succeeded request_id={request_id} "
            f"nodes={len(candidate_doc.nodes)} rels={len(candidate_doc.relationships)} "
            f"latency_ms={provider_resp.latency_ms}"
        )

        return candidate_doc, provider_resp

