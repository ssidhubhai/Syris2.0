import json
import pytest
from pathlib import Path
from backend.app.providers.base import ModelNotCertifiedException
from backend.app.schemas.explanation import (
    ExplanationDocumentSchema,
    ExplanationNodeSchema,
    RelationshipSchema,
)
from backend.evals.failure_taxonomy import FAILURE_DEFINITIONS, make_failure_item
from backend.evals.latency_tracer import LatencyTracer
from backend.evals.metrics import MetricsEvaluator
from backend.evals.run_evaluation import (
    EvaluationDatasetLoader,
    EvaluationRunner,
    MockEvaluationProvider,
)
from backend.evals.schemas import (
    EvaluationCase,
    HumanReviewFlags,
    HumanReviewScorecard,
)
from backend.evals.scorecard import ScorecardManager


def test_seed_dataset_integrity():
    """Verifies that all 54 seed evaluation cases load cleanly and have unique IDs."""
    cases = EvaluationDatasetLoader.load_all_cases()
    assert len(cases) == 54, f"Expected 54 cases, found {len(cases)}"

    ids = [c.id for c in cases]
    assert len(ids) == len(set(ids)), "Duplicate case IDs detected in seed dataset"

    # Category and Subject breakdown verification
    subjects = {c.subject for c in cases}
    assert subjects == {"physics", "chemistry", "mathematics"}

    phy_cases = [c for c in cases if c.subject == "physics"]
    math_cases = [c for c in cases if c.subject == "mathematics"]
    chem_cases = [c for c in cases if c.subject == "chemistry"]

    assert len(phy_cases) == 22  # 15 physics + 4 hinglish + 3 compact
    assert len(math_cases) == 15  # 13 math + 1 hinglish + 1 compact
    assert len(chem_cases) == 17  # 13 chem + 3 hinglish + 1 compact
    assert len(phy_cases) + len(math_cases) + len(chem_cases) == 54



def test_dataset_filtering():
    """Verifies filtering by ID, subject, category, and limit."""
    all_cases = EvaluationDatasetLoader.load_all_cases()

    # Filter by ID
    res = EvaluationDatasetLoader.filter_cases(all_cases, ids=["eval-phy-001", "eval-math-001"])
    assert len(res) == 2
    assert {c.id for c in res} == {"eval-phy-001", "eval-math-001"}

    # Filter by Subject
    res_chem = EvaluationDatasetLoader.filter_cases(all_cases, subject="chemistry")
    assert len(res_chem) > 0
    assert all(c.subject == "chemistry" for c in res_chem)

    # Filter by Category & Limit
    res_lim = EvaluationDatasetLoader.filter_cases(all_cases, category="conceptual", limit=3)
    assert len(res_lim) == 3


def test_latency_tracer():
    """Verifies LatencyTracer records stage and total timings."""
    tracer = LatencyTracer()
    tracer.start_stage("preprocessing")
    tracer.end_stage("preprocessing")
    tracer.start_stage("gemini_request")
    tracer.end_stage("gemini_request")
    total = tracer.finish_total()

    assert total >= 0.0
    bd = tracer.to_breakdown()
    assert bd.total_pipeline_time_ms == total
    assert "preprocessing" in tracer.summary_dict()


def test_human_scorecard_and_critical_error_override():
    """Verifies HumanReviewScorecard grading and critical error override."""
    scorecard = HumanReviewScorecard(
        reviewer="test_evaluator",
        case_id="eval-phy-001",
        factual_correctness=5,
        reasoning_continuity=5,
        pedagogical_clarity=5,
        appropriate_detail=5,
        visual_usefulness=5,
        relationship_clarity=5,
        language_naturalness=5,
        jee_relevance=5,
        flags=HumanReviewFlags(critical_error=False),
    )
    assert scorecard.composite_average == 5.0
    assert scorecard.effective_grade == "EXCELLENT"

    # Flag critical error -> must override average to CRITICAL_FAIL
    scorecard.flags.critical_error = True
    assert scorecard.effective_grade == "CRITICAL_FAIL"


def test_scorecard_persistence(tmp_path: Path):
    """Verifies ScorecardManager saves and loads scorecard files."""
    manager = ScorecardManager(storage_dir=tmp_path)
    scorecard = HumanReviewScorecard(
        reviewer="test_evaluator",
        case_id="eval-math-002",
        factual_correctness=4,
        reasoning_continuity=4,
        pedagogical_clarity=4,
        appropriate_detail=4,
        visual_usefulness=4,
        relationship_clarity=4,
        language_naturalness=4,
        jee_relevance=4,
    )
    saved_path = manager.save_scorecard(scorecard)
    assert saved_path.exists()

    loaded = manager.load_scorecard(case_id="eval-math-002", reviewer="test_evaluator")
    assert loaded is not None
    assert loaded.case_id == "eval-math-002"
    assert loaded.composite_average == 4.0


def test_failure_taxonomy_definitions():
    """Verifies standardized failure taxonomy codes and constructors."""
    assert len(FAILURE_DEFINITIONS) == 10
    item = make_failure_item("A_BAD_PRESENTATION", "Custom detail")
    assert item.category_code == "A_BAD_PRESENTATION"
    assert item.title == "Correct but Badly Presented"
    assert item.description == "Custom detail"


def test_automated_metrics_evaluation():
    """Verifies automated structural, complexity, and presentation metric computation."""
    cases = EvaluationDatasetLoader.load_all_cases()
    case = cases[0]  # eval-phy-001

    doc = ExplanationDocumentSchema(
        document_id="doc-test-1",
        session_id="sess-test-1",
        title="Lenz Law Concept",
        intent="concept_explanation",
        subject="physics",
        language="english",
        nodes=[
            ExplanationNodeSchema(id="n-1", type="heading", content={"text": "Lenz Law"}),
            ExplanationNodeSchema(id="n-2", type="definition", content={"title": "Lenz Law", "latex": "\\mathcal{E} = -\\frac{d\\Phi}{dt}"}),
            ExplanationNodeSchema(id="n-3", type="conclusion", content={"title": "Conservation of Energy"}),
        ],
        relationships=[
            RelationshipSchema(**{"from": "n-1", "to": "n-2", "type": "defines"}),
            RelationshipSchema(**{"from": "n-2", "to": "n-3", "type": "explains"}),
        ],
    )

    metrics, failures = MetricsEvaluator.evaluate(case=case, doc=doc)
    assert metrics.structural.schema_valid is True
    assert metrics.structural.node_id_integrity is True
    assert metrics.structural.relationship_integrity is True
    assert metrics.complexity.node_count == 3
    assert metrics.complexity.relationship_count == 2
    assert metrics.presentation.representation_compatibility in ("exact_match", "pedagogically_acceptable")


@pytest.mark.asyncio
async def test_mock_evaluation_runner(tmp_path: Path):
    """Verifies Mock Evaluation Runner runs suite and generates artifacts."""
    cases = EvaluationDatasetLoader.load_all_cases()[:3]
    runner = EvaluationRunner(mode="mock", output_dir=tmp_path)
    report = await runner.run_suite(cases)

    assert report.total_cases_evaluated == 3
    assert report.successful_cases == 3
    assert report.failed_cases == 0
    assert (tmp_path / "results.json").exists()
    assert (tmp_path / "summary.md").exists()
    assert (tmp_path / "digital_paper_samples").exists()


def test_runner_rejects_uncertified_model():
    """Verifies runner fails closed if an uncertified model is supplied in live mode."""
    with pytest.raises(ModelNotCertifiedException):
        EvaluationRunner(mode="live_gemini", model_id="uncertified-random-model-xyz")
