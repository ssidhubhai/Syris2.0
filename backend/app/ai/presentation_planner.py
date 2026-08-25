from typing import Literal, Optional
from pydantic import BaseModel, Field
from backend.app.ai.context_analyzer import AnalysisContext

PresentationStrategy = Literal[
    "COMPACT_EXPLANATION",
    "CONCEPT_CENTRIC",
    "DERIVATION_CENTRIC",
    "DIAGRAM_CENTRIC",
    "COMPARISON",
    "SEQUENTIAL_TRANSFORMATION",
    "MIXED_EXPLANATION",
]


class PresentationPlan(BaseModel):
    """
    Semantic presentation strategy determined for the student question.
    Guides the single-stage generation and provides layout hints for the CompositionEngine.
    """
    strategy: PresentationStrategy = Field(
        default="CONCEPT_CENTRIC",
        description="Core semantic composition archetype",
    )
    needs_diagram: bool = Field(
        default=False,
        description="Whether a visual diagram or FBD is essential to reduce cognitive load",
    )
    needs_equations: bool = Field(
        default=False,
        description="Whether mathematical formulas or equilibrium equations are required",
    )
    needs_comparison: bool = Field(
        default=False,
        description="Whether a side-by-side comparison structure is required",
    )
    needs_derivation_steps: bool = Field(
        default=False,
        description="Whether sequential derivation steps with algebraic reasons are required",
    )
    recommended_layout: str = Field(
        default="auto",
        description="Recommended layout preference: auto, hybrid_dual_channel, split_columns, sequential_flow",
    )
    justification: str = Field(
        default="",
        description="Pedagogical rationale for this presentation strategy",
    )


class PresentationPlanner:
    """
    Semantic Presentation Planner for Syris 2.0.
    Enforces non-negotiable rule: NEVER use a universal template (e.g. text + diagram + flowchart + equation).
    Decides representation strategy dynamically based on subject, intent, and cognitive complexity.
    """

    @classmethod
    def plan(cls, context: AnalysisContext) -> PresentationPlan:
        # 1. Comparison Queries (e.g. SN1 vs SN2)
        if context.intent == "comparison" or context.detected_visual_need == "comparison_table":
            return PresentationPlan(
                strategy="COMPARISON",
                needs_diagram=False,
                needs_equations=False,
                needs_comparison=True,
                needs_derivation_steps=False,
                recommended_layout="split_columns",
                justification="Direct side-by-side comparison reduces cognitive load for contrasting mechanisms.",
            )

        # 2. Simple Definitions (e.g. What is centripetal acceleration?)
        if context.intent == "definition" and context.complexity == "low":
            return PresentationPlan(
                strategy="COMPACT_EXPLANATION",
                needs_diagram=False,
                needs_equations=True,
                needs_comparison=False,
                needs_derivation_steps=False,
                recommended_layout="auto",
                justification="Compact definition with core formula; visual diagram is unnecessary and bloated.",
            )

        # 3. Derivations & Mathematical Proofs
        if context.intent == "derivation" or context.detected_visual_need == "derivation_flow":
            return PresentationPlan(
                strategy="DERIVATION_CENTRIC",
                needs_diagram=False,
                needs_equations=True,
                needs_comparison=False,
                needs_derivation_steps=True,
                recommended_layout="sequential_flow",
                justification="Step-by-step mathematical derivation with isolated equations and justification steps.",
            )

        # 4. Mechanics / Problem Solving with Geometric System
        if context.detected_visual_need == "diagram" or (context.subject == "physics" and context.intent == "problem_solving"):
            return PresentationPlan(
                strategy="DIAGRAM_CENTRIC",
                needs_diagram=True,
                needs_equations=True,
                needs_comparison=False,
                needs_derivation_steps=True,
                recommended_layout="hybrid_dual_channel",
                justification="Spatial force resolution requires visual context alongside equilibrium equations.",
            )

        # 5. Default: Concept Explanation
        return PresentationPlan(
            strategy="CONCEPT_CENTRIC",
            needs_diagram=False,
            needs_equations=True,
            needs_comparison=False,
            needs_derivation_steps=False,
            recommended_layout="auto",
            justification="Focused conceptual explanation with governing laws and key takeaways.",
        )
