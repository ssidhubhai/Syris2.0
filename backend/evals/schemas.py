from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field


class GoldenExpectation(BaseModel):
    """Pedagogical and visual expectations for an evaluation case."""
    min_required_concepts: List[str] = Field(default_factory=list)
    forbidden_misconceptions: List[str] = Field(default_factory=list)
    visual_utility: Literal["essential", "helpful", "redundant_decorative"] = "helpful"
    expected_depth: Literal["concise", "standard", "deep_derivation"] = "standard"
    expected_relationship_types: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="ignore")


class EvaluationCase(BaseModel):
    """A single curated evaluation question with metadata and golden expectations."""
    id: str
    subject: Literal["physics", "chemistry", "mathematics", "general"]
    category: Literal["conceptual", "derivation", "diagram", "comparison", "mechanism", "hinglish", "compact"]
    question: str
    expected_intent: str
    expected_complexity: Literal["foundational", "intermediate", "advanced_jee"]
    expected_representation_preference: str
    visual_expected: Literal["yes", "no", "maybe"] = "maybe"
    key_concepts: List[str] = Field(default_factory=list)
    critical_relationships: List[str] = Field(default_factory=list)
    known_traps: List[str] = Field(default_factory=list)
    expected_language: Literal["english", "hinglish"] = "english"
    golden: GoldenExpectation

    model_config = ConfigDict(extra="ignore")


# ============================================================
# AUTOMATED METRICS SCHEMAS
# ============================================================

class StructuralMetrics(BaseModel):
    schema_valid: bool = True
    node_id_integrity: bool = True
    relationship_integrity: bool = True
    empty_node_rate: float = 0.0
    duplicate_node_ids: int = 0
    dangling_relationships: int = 0
    self_loop_relationships: int = 0


class PresentationMetrics(BaseModel):
    visual_appropriateness_signal: Literal["appropriate", "unnecessary_visual", "missing_visual", "neutral"] = "neutral"
    unnecessary_visual_signal: bool = False
    missing_visual_signal: bool = False
    representation_compatibility: Literal["exact_match", "pedagogically_acceptable", "divergent"] = "pedagogically_acceptable"
    composition_coverage: float = 1.0


class ComplexityMetrics(BaseModel):
    node_count: int = 0
    relationship_count: int = 0
    total_word_count: int = 0
    equation_count: int = 0
    diagram_count: int = 0
    derivation_step_count: int = 0
    comparison_count: int = 0
    callout_count: int = 0


class ReliabilityMetrics(BaseModel):
    total_latency_ms: float = 0.0
    provider_error_rate: float = 0.0
    malformed_output_rate: float = 0.0
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class ConceptSignalMetrics(BaseModel):
    matched_concepts: List[str] = Field(default_factory=list)
    missing_concepts: List[str] = Field(default_factory=list)
    concept_coverage_rate: float = 0.0
    detected_forbidden_misconceptions: List[str] = Field(default_factory=list)


class LatencyBreakdown(BaseModel):
    preprocessing_time_ms: float = 0.0
    prompt_prep_time_ms: float = 0.0
    gemini_request_time_ms: float = 0.0
    response_parse_time_ms: float = 0.0
    validation_time_ms: float = 0.0
    persistence_time_ms: float = 0.0
    total_pipeline_time_ms: float = 0.0


class AutomatedMetrics(BaseModel):
    structural: StructuralMetrics = Field(default_factory=StructuralMetrics)
    presentation: PresentationMetrics = Field(default_factory=PresentationMetrics)
    complexity: ComplexityMetrics = Field(default_factory=ComplexityMetrics)
    reliability: ReliabilityMetrics = Field(default_factory=ReliabilityMetrics)
    concept_signal: ConceptSignalMetrics = Field(default_factory=ConceptSignalMetrics)
    latency_breakdown: LatencyBreakdown = Field(default_factory=LatencyBreakdown)


# ============================================================
# HUMAN SCORECARD & FAILURE TAXONOMY SCHEMAS
# ============================================================

class HumanReviewFlags(BaseModel):
    critical_error: bool = False
    minor_error: bool = False
    unnecessary_content: bool = False
    missing_reasoning: bool = False
    misleading_visual: bool = False
    awkward_hinglish: bool = False


class HumanReviewScorecard(BaseModel):
    """
    Standard human evaluation scorecard on 1-5 scale across 8 dimensions.
    Critical errors override composite aggregate averages.
    """
    reviewer: str = "evaluator"
    case_id: str
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # 1-5 Numerical Scores
    factual_correctness: int = Field(ge=1, le=5, description="1: Wrong -> 5: Mathematically & physically exact")
    reasoning_continuity: int = Field(ge=1, le=5, description="1: Disjoint -> 5: Step-by-step causal derivation")
    pedagogical_clarity: int = Field(ge=1, le=5, description="1: Confusing -> 5: Clear, intuitive concept building")
    appropriate_detail: int = Field(ge=1, le=5, description="1: Bloated/Terse -> 5: Ideal cognitive sizing")
    visual_usefulness: int = Field(ge=1, le=5, description="1: Distracting/Useless -> 5: Essential explanatory leverage")
    relationship_clarity: int = Field(ge=1, le=5, description="1: Broken/Missing -> 5: Precise semantic links")
    language_naturalness: int = Field(ge=1, le=5, description="1: Robotic/Awkward -> 5: Fluent English/Hinglish")
    jee_relevance: int = Field(ge=1, le=5, description="1: Superficial -> 5: Authentic JEE Advanced standard")

    flags: HumanReviewFlags = Field(default_factory=HumanReviewFlags)
    notes: Optional[str] = None

    @property
    def composite_average(self) -> float:
        scores = [
            self.factual_correctness,
            self.reasoning_continuity,
            self.pedagogical_clarity,
            self.appropriate_detail,
            self.visual_usefulness,
            self.relationship_clarity,
            self.language_naturalness,
            self.jee_relevance,
        ]
        return round(sum(scores) / len(scores), 2)

    @property
    def effective_grade(self) -> str:
        if self.flags.critical_error:
            return "CRITICAL_FAIL"
        avg = self.composite_average
        if avg >= 4.5:
            return "EXCELLENT"
        elif avg >= 3.8:
            return "GOOD"
        elif avg >= 3.0:
            return "ACCEPTABLE"
        else:
            return "DEFICIENT"


FailureCode = Literal[
    "A_BAD_PRESENTATION",
    "B_INCORRECT_REASONING",
    "C_MISSING_CONCEPT",
    "D_UNNECESSARY_VISUAL",
    "E_MISSING_USEFUL_VISUAL",
    "F_BROKEN_RELATIONSHIPS",
    "G_TOO_VERBOSE",
    "H_TOO_TERSE",
    "I_AWKWARD_LANGUAGE",
    "J_SCHEMA_FAILURE",
]


class CaseFailureItem(BaseModel):
    category_code: FailureCode
    title: str
    description: str


# ============================================================
# EVALUATION RESULT & RUN REPORT SCHEMAS
# ============================================================

class EvaluationCaseResult(BaseModel):
    case_id: str
    subject: str
    category: str
    question: str
    model_id: str
    prompt_version: str = "v1.0"
    success: bool
    error_message: Optional[str] = None
    document: Optional[Dict[str, Any]] = None
    metrics: AutomatedMetrics = Field(default_factory=AutomatedMetrics)
    failures: List[CaseFailureItem] = Field(default_factory=list)
    human_scorecard: Optional[HumanReviewScorecard] = None


class ModelComparisonSummary(BaseModel):
    model_id: str
    total_cases: int
    success_count: int
    failure_count: int
    avg_latency_ms: float
    avg_node_count: float
    avg_relationship_count: float
    avg_concept_coverage_rate: float
    unnecessary_visual_count: int
    missing_visual_count: int
    critical_error_count: int


class EvaluationRunReport(BaseModel):
    run_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    mode: Literal["mock", "live_gemini"]
    model_ids: List[str]
    prompt_version: str
    total_cases_evaluated: int
    successful_cases: int
    failed_cases: int
    case_results: List[EvaluationCaseResult] = Field(default_factory=list)
    model_summaries: List[ModelComparisonSummary] = Field(default_factory=list)
    latency_summary: Dict[str, float] = Field(default_factory=dict)
    failure_distribution: Dict[str, int] = Field(default_factory=dict)
