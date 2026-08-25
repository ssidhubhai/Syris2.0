import pytest
from backend.app.ai.context_analyzer import ContextAnalyzer


def test_context_analyzer_physics_mechanics_problem():
    query = "Why is friction acting downward on the wedge?"
    context = ContextAnalyzer.analyze(query)

    assert context.subject == "physics"
    assert context.intent in ("concept_explanation", "problem_solving")
    assert context.detected_visual_need in ("diagram", "none")
    assert "friction" in context.key_entities or "wedge" in context.key_entities


def test_context_analyzer_compact_definition():
    query = "What is centripetal acceleration?"
    context = ContextAnalyzer.analyze(query)

    assert context.subject == "physics"
    assert context.intent == "definition"
    assert context.complexity == "low"
    assert context.detected_visual_need == "none"


def test_context_analyzer_chemistry_comparison():
    query = "What is the difference between SN1 and SN2 reactions?"
    context = ContextAnalyzer.analyze(query)

    assert context.subject == "chemistry"
    assert context.intent == "comparison"
    assert context.detected_visual_need == "comparison_table"


def test_context_analyzer_math_derivation():
    query = "Evaluate definite integral using Feynman's trick step by step"
    context = ContextAnalyzer.analyze(query)

    assert context.subject == "mathematics"
    assert context.intent == "derivation"
    assert context.requested_help_level == "step_by_step"
    assert context.detected_visual_need == "derivation_flow"


def test_context_analyzer_hinglish_detection():
    query = "Block jab accelerate karega toh pseudo force kaise lagega?"
    context = ContextAnalyzer.analyze(query)

    assert context.language == "hinglish"
    assert context.subject == "physics"
