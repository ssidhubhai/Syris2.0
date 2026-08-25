import pytest
from backend.app.ai.context_analyzer import AnalysisContext
from backend.app.ai.presentation_planner import PresentationPlanner


def test_presentation_planner_comparison_strategy():
    ctx = AnalysisContext(
        intent="comparison",
        subject="chemistry",
        complexity="medium",
        detected_visual_need="comparison_table",
    )
    plan = PresentationPlanner.plan(ctx)

    assert plan.strategy == "COMPARISON"
    assert plan.needs_comparison is True
    assert plan.needs_diagram is False


def test_presentation_planner_compact_definition_no_diagram():
    ctx = AnalysisContext(
        intent="definition",
        subject="physics",
        complexity="low",
        detected_visual_need="none",
    )
    plan = PresentationPlanner.plan(ctx)

    assert plan.strategy == "COMPACT_EXPLANATION"
    assert plan.needs_diagram is False
    assert plan.needs_equations is True
    assert plan.needs_derivation_steps is False


def test_presentation_planner_derivation_flow():
    ctx = AnalysisContext(
        intent="derivation",
        subject="mathematics",
        complexity="high",
        detected_visual_need="derivation_flow",
    )
    plan = PresentationPlanner.plan(ctx)

    assert plan.strategy == "DERIVATION_CENTRIC"
    assert plan.needs_derivation_steps is True
    assert plan.needs_diagram is False


def test_presentation_planner_diagram_centric_problem():
    ctx = AnalysisContext(
        intent="problem_solving",
        subject="physics",
        complexity="high",
        detected_visual_need="diagram",
    )
    plan = PresentationPlanner.plan(ctx)

    assert plan.strategy == "DIAGRAM_CENTRIC"
    assert plan.needs_diagram is True
    assert plan.needs_equations is True
