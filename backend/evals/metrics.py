import re
from typing import Any, Dict, List, Optional, Set, Tuple
from backend.app.schemas.explanation import ExplanationDocumentSchema, ExplanationNodeSchema
from backend.evals.failure_taxonomy import make_failure_item
from backend.evals.schemas import (
    AutomatedMetrics,
    CaseFailureItem,
    ComplexityMetrics,
    ConceptSignalMetrics,
    EvaluationCase,
    LatencyBreakdown,
    PresentationMetrics,
    ReliabilityMetrics,
    StructuralMetrics,
)


# Strategy compatibility mapping: preferred strategy -> set of acceptable strategies
STRATEGY_COMPATIBILITY: Dict[str, Set[str]] = {
    "COMPACT_EXPLANATION": {"COMPACT_EXPLANATION", "CONCEPT_CENTRIC"},
    "CONCEPT_CENTRIC": {"CONCEPT_CENTRIC", "COMPACT_EXPLANATION", "MIXED_EXPLANATION"},
    "DERIVATION_CENTRIC": {"DERIVATION_CENTRIC", "SEQUENTIAL_TRANSFORMATION", "MIXED_EXPLANATION"},
    "DIAGRAM_CENTRIC": {"DIAGRAM_CENTRIC", "MIXED_EXPLANATION"},
    "COMPARISON": {"COMPARISON", "MIXED_EXPLANATION", "CONCEPT_CENTRIC"},
    "SEQUENTIAL_TRANSFORMATION": {"SEQUENTIAL_TRANSFORMATION", "DERIVATION_CENTRIC", "MIXED_EXPLANATION"},
    "MIXED_EXPLANATION": {
        "MIXED_EXPLANATION",
        "CONCEPT_CENTRIC",
        "DERIVATION_CENTRIC",
        "DIAGRAM_CENTRIC",
        "COMPARISON",
        "SEQUENTIAL_TRANSFORMATION",
    },
}


class MetricsEvaluator:
    """
    Computes objective quantitative metrics and automated quality signals
    from an ExplanationDocument against an EvaluationCase's golden expectations.
    """

    @classmethod
    def evaluate(
        cls,
        case: EvaluationCase,
        doc: Optional[ExplanationDocumentSchema],
        latency_breakdown: Optional[LatencyBreakdown] = None,
        raw_error: Optional[str] = None,
        token_usage: Optional[Dict[str, int]] = None,
    ) -> Tuple[AutomatedMetrics, List[CaseFailureItem]]:
        failures: List[CaseFailureItem] = []
        breakdown = latency_breakdown or LatencyBreakdown()

        if doc is None or raw_error is not None:
            # Handle catastrophic generation failure
            failures.append(
                make_failure_item(
                    "J_SCHEMA_FAILURE",
                    f"Model generation or validation failed: {raw_error or 'No document produced'}",
                )
            )
            return (
                AutomatedMetrics(
                    structural=StructuralMetrics(schema_valid=False),
                    reliability=ReliabilityMetrics(
                        total_latency_ms=breakdown.total_pipeline_time_ms,
                        provider_error_rate=1.0 if raw_error else 0.0,
                        malformed_output_rate=1.0 if not raw_error else 0.0,
                    ),
                    latency_breakdown=breakdown,
                ),
                failures,
            )

        # 1. Compute Structural Metrics
        structural, struct_failures = cls._compute_structural_metrics(doc)
        failures.extend(struct_failures)

        # 2. Compute Complexity Metrics
        complexity = cls._compute_complexity_metrics(doc)

        # 3. Compute Presentation Metrics
        presentation, pres_failures = cls._compute_presentation_metrics(case, doc, complexity)
        failures.extend(pres_failures)

        # 4. Compute Concept Signal Metrics (SIGNAL ONLY, not factual correctness)
        concept_signal, concept_failures = cls._compute_concept_signals(case, doc)
        failures.extend(concept_failures)

        # 5. Compute Reliability Metrics
        tokens = token_usage or {}
        reliability = ReliabilityMetrics(
            total_latency_ms=breakdown.total_pipeline_time_ms,
            provider_error_rate=0.0,
            malformed_output_rate=0.0,
            input_tokens=tokens.get("input_tokens"),
            output_tokens=tokens.get("output_tokens"),
            total_tokens=tokens.get("total_tokens"),
        )

        metrics = AutomatedMetrics(
            structural=structural,
            presentation=presentation,
            complexity=complexity,
            reliability=reliability,
            concept_signal=concept_signal,
            latency_breakdown=breakdown,
        )

        return metrics, failures

    @classmethod
    def _compute_structural_metrics(
        cls, doc: ExplanationDocumentSchema
    ) -> Tuple[StructuralMetrics, List[CaseFailureItem]]:
        failures: List[CaseFailureItem] = []
        node_ids: Set[str] = set()
        duplicate_ids = 0
        empty_nodes = 0

        for node in doc.nodes:
            if not node.id or not node.id.strip():
                duplicate_ids += 1
            elif node.id in node_ids:
                duplicate_ids += 1
            else:
                node_ids.add(node.id)

            if cls._is_node_empty(node):
                empty_nodes += 1

        empty_rate = round(empty_nodes / len(doc.nodes), 3) if doc.nodes else 0.0

        dangling_rels = 0
        self_loops = 0
        for rel in doc.relationships:
            if rel.from_node == rel.to_node:
                self_loops += 1
            if rel.from_node not in node_ids or rel.to_node not in node_ids:
                dangling_rels += 1

        node_integrity = (duplicate_ids == 0) and (empty_nodes == 0)
        rel_integrity = (dangling_rels == 0) and (self_loops == 0)

        if not rel_integrity:
            failures.append(
                make_failure_item(
                    "F_BROKEN_RELATIONSHIPS",
                    f"Found {dangling_rels} dangling relationships and {self_loops} self-loops.",
                )
            )

        return (
            StructuralMetrics(
                schema_valid=True,
                node_id_integrity=node_integrity,
                relationship_integrity=rel_integrity,
                empty_node_rate=empty_rate,
                duplicate_node_ids=duplicate_ids,
                dangling_relationships=dangling_rels,
                self_loop_relationships=self_loops,
            ),
            failures,
        )

    @classmethod
    def _compute_complexity_metrics(cls, doc: ExplanationDocumentSchema) -> ComplexityMetrics:
        node_count = len(doc.nodes)
        rel_count = len(doc.relationships)
        total_words = 0
        eq_count = 0
        diag_count = 0
        deriv_count = 0
        comp_count = 0
        callout_count = 0

        for node in doc.nodes:
            text_repr = cls._extract_node_text(node)
            words = re.findall(r"\b\w+\b", text_repr)
            total_words += len(words)

            if node.type == "equation":
                eq_count += 1
            elif node.type == "diagram":
                diag_count += 1
            elif node.type == "derivation_step":
                deriv_count += 1
            elif node.type == "comparison":
                comp_count += 1
            elif node.type == "callout":
                callout_count += 1

        return ComplexityMetrics(
            node_count=node_count,
            relationship_count=rel_count,
            total_word_count=total_words,
            equation_count=eq_count,
            diagram_count=diag_count,
            derivation_step_count=deriv_count,
            comparison_count=comp_count,
            callout_count=callout_count,
        )

    @classmethod
    def _compute_presentation_metrics(
        cls,
        case: EvaluationCase,
        doc: ExplanationDocumentSchema,
        complexity: ComplexityMetrics,
    ) -> Tuple[PresentationMetrics, List[CaseFailureItem]]:
        failures: List[CaseFailureItem] = []
        has_diagram = complexity.diagram_count > 0

        # Visual appropriateness signal
        unnecessary_visual = False
        missing_visual = False
        vis_signal = "neutral"

        if case.visual_expected == "no" and has_diagram:
            unnecessary_visual = True
            vis_signal = "unnecessary_visual"
            failures.append(
                make_failure_item(
                    "D_UNNECESSARY_VISUAL",
                    "Generated a diagram node for a non-visual conceptual/definition question.",
                )
            )
        elif case.visual_expected == "yes" and not has_diagram:
            missing_visual = True
            vis_signal = "missing_visual"
            failures.append(
                make_failure_item(
                    "E_MISSING_USEFUL_VISUAL",
                    "Omitted visual representation for a spatial, geometry, or ray-tracing case.",
                )
            )
        elif case.visual_expected in ("yes", "no"):
            vis_signal = "appropriate"

        # Representation compatibility (flexible golden presentation principle)
        layout_hint = doc.layout_hints.recommended_layout if doc.layout_hints else None
        actual_layout = (layout_hint or "CONCEPT_CENTRIC").upper()
        preferred = case.expected_representation_preference.upper()
        allowed_alternatives = STRATEGY_COMPATIBILITY.get(preferred, {preferred})


        if actual_layout == preferred:
            rep_compat = "exact_match"
        elif actual_layout in allowed_alternatives:
            rep_compat = "pedagogically_acceptable"
        else:
            rep_compat = "divergent"

        # Composition plan coverage (ratio of required node types present)
        # For derivation: expects derivation_step or equation
        # For comparison: expects comparison node
        expected_type_found = True
        if preferred == "DERIVATION_CENTRIC" and (complexity.derivation_step_count == 0 and complexity.equation_count == 0):
            expected_type_found = False
        elif preferred == "COMPARISON" and complexity.comparison_count == 0:
            expected_type_found = False

        coverage = 1.0 if expected_type_found else 0.5

        # Check extreme verbosity / terseness signals
        if complexity.total_word_count > 900:
            failures.append(
                make_failure_item(
                    "G_TOO_VERBOSE",
                    f"Generated {complexity.total_word_count} words, risking student cognitive overload.",
                )
            )
        elif complexity.total_word_count < 30 and case.category != "compact":
            failures.append(
                make_failure_item(
                    "H_TOO_TERSE",
                    f"Generated only {complexity.total_word_count} words with insufficient conceptual depth.",
                )
            )

        return (
            PresentationMetrics(
                visual_appropriateness_signal=vis_signal,
                unnecessary_visual_signal=unnecessary_visual,
                missing_visual_signal=missing_visual,
                representation_compatibility=rep_compat,
                composition_coverage=coverage,
            ),
            failures,
        )

    @classmethod
    def _compute_concept_signals(
        cls, case: EvaluationCase, doc: ExplanationDocumentSchema
    ) -> Tuple[ConceptSignalMetrics, List[CaseFailureItem]]:
        """
        Calculates concept presence as an exploratory SIGNAL only.
        Matches keywords and checks for known misconceptions.
        """
        failures: List[CaseFailureItem] = []
        doc_text = " ".join([cls._extract_node_text(n) for n in doc.nodes]).lower()

        matched: List[str] = []
        missing: List[str] = []

        for concept in case.golden.min_required_concepts:
            # Check individual words of concept phrase
            concept_clean = concept.lower()
            tokens = [t for t in re.findall(r"\b\w+\b", concept_clean) if len(t) > 2]
            if not tokens or any(t in doc_text for t in tokens):
                matched.append(concept)
            else:
                missing.append(concept)

        coverage_rate = round(len(matched) / len(case.golden.min_required_concepts), 2) if case.golden.min_required_concepts else 1.0

        if coverage_rate < 0.3:
            failures.append(
                make_failure_item(
                    "C_MISSING_CONCEPT",
                    f"Missing core golden concepts: {', '.join(missing[:3])}",
                )
            )

        # Misconception check
        detected_misconceptions: List[str] = []
        for trap in case.golden.forbidden_misconceptions:
            trap_tokens = [t for t in re.findall(r"\b\w+\b", trap.lower()) if len(t) > 3]
            if len(trap_tokens) >= 3 and all(t in doc_text for t in trap_tokens[:3]):
                detected_misconceptions.append(trap)
                failures.append(
                    make_failure_item(
                        "B_INCORRECT_REASONING",
                        f"Potential forbidden misconception detected: '{trap}'",
                    )
                )

        return (
            ConceptSignalMetrics(
                matched_concepts=matched,
                missing_concepts=missing,
                concept_coverage_rate=coverage_rate,
                detected_forbidden_misconceptions=detected_misconceptions,
            ),
            failures,
        )

    @classmethod
    def _is_node_empty(cls, node: ExplanationNodeSchema) -> bool:
        """Returns True if a node has no meaningful textual or mathematical content."""
        content = node.content
        if isinstance(content, dict):
            for v in content.values():
                if v and str(v).strip():
                    return False
            return True
        elif hasattr(content, "model_dump"):
            dump = content.model_dump()
            for v in dump.values():
                if v and str(v).strip():
                    return False
            return True
        return not bool(content)

    @classmethod
    def _extract_node_text(cls, node: ExplanationNodeSchema) -> str:
        """Extracts all string tokens from a node content object."""
        content = node.content
        if isinstance(content, dict):
            parts = []
            for k, v in content.items():
                if isinstance(v, str):
                    parts.append(v)
                elif isinstance(v, list):
                    parts.extend([str(item) for item in v])
            return " ".join(parts)
        elif hasattr(content, "model_dump"):
            dump = content.model_dump()
            parts = []
            for k, v in dump.items():
                if isinstance(v, str):
                    parts.append(v)
                elif isinstance(v, list):
                    parts.extend([str(item) for item in v])
            return " ".join(parts)
        return str(content)
