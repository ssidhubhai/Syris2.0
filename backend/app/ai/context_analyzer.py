import re
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

SubjectType = Literal["physics", "chemistry", "mathematics", "general"]
ComplexityType = Literal["low", "medium", "high"]
VisualNeedType = Literal["none", "diagram", "graph", "comparison_table", "derivation_flow"]


class AnalysisContext(BaseModel):
    """
    Internal structured context representing the student query.
    Extracted deterministically to enrich the single-stage generation prompt.
    """
    intent: str = Field(
        default="concept_explanation",
        description="Primary intent: concept_explanation, problem_solving, derivation, comparison, definition",
    )
    subject: SubjectType = Field(
        default="physics",
        description="Classified subject: physics, chemistry, mathematics, general",
    )
    complexity: ComplexityType = Field(
        default="medium",
        description="Assessed complexity level for JEE preparation",
    )
    language: str = Field(
        default="hinglish",
        description="Primary language mode: hinglish, english",
    )
    requested_help_level: Literal["explain", "hint", "step_by_step", "deep_dive"] = Field(
        default="explain",
        description="Requested pedagogical depth",
    )
    detected_visual_need: VisualNeedType = Field(
        default="none",
        description="Visual representation necessity",
    )
    key_entities: List[str] = Field(
        default_factory=list,
        description="Extracted domain keywords and physics/chem/math entities",
    )
    user_goal: str = Field(
        default="understand_concept",
        description="Concise description of the student's learning objective",
    )


class ContextAnalyzer:
    """
    Deterministic Context Analyzer for V1.
    Performs fast heuristic classification to guide the single structured model prompt.
    """

    CHEMISTRY_KEYWORDS = {
        "sn1", "sn2", "electrophile", "nucleophile", "carbocation", "hybridization",
        "orbital", "reaction", "organic", "inorganic", "isomerism", "equilibrium",
        "thermodynamics", "electrochemistry", "coordination", "enthalpy", "entropy",
        "acid", "base", "ph", "pka", "solubility", "le chatelier", "markovnikov",
    }

    MATH_KEYWORDS = {
        "integral", "derivative", "differentiation", "integration", "matrix", "determinant",
        "vector", "3d geometry", "complex number", "probability", "permutation",
        "combination", "binomial", "quadratic", "limit", "continuity", "feynman",
        "frullani", "taylor series", "differential equation",
    }

    PHYSICS_KEYWORDS = {
        "friction", "wedge", "incline", "acceleration", "centripetal", "velocity",
        "gravity", "force", "pseudo force", "torque", "rotation", "moment of inertia",
        "momentum", "collision", "work", "energy", "potential", "electric field",
        "magnetic field", "flux", "induction", "optics", "refraction", "interference",
        "shm", "wave", "capacitance", "current", "thermodynamics",
    }

    @classmethod
    def analyze(cls, text: str) -> AnalysisContext:
        """
        Extracts AnalysisContext from query using deterministic linguistic heuristics.
        """
        normalized = text.lower().strip()
        words = set(re.findall(r"\b\w+\b", normalized))

        # 1. Subject Classification
        subject: SubjectType = "general"
        chem_matches = len(words.intersection(cls.CHEMISTRY_KEYWORDS))
        math_matches = len(words.intersection(cls.MATH_KEYWORDS))
        phys_matches = len(words.intersection(cls.PHYSICS_KEYWORDS))

        if chem_matches > math_matches and chem_matches > phys_matches:
            subject = "chemistry"
        elif math_matches > chem_matches and math_matches > phys_matches:
            subject = "mathematics"
        elif phys_matches > 0:
            subject = "physics"
        else:
            # Default to physics for mechanics / general questions
            subject = "physics"

        # 2. Intent & Visual Need Classification
        intent = "concept_explanation"
        visual_need: VisualNeedType = "none"
        complexity: ComplexityType = "medium"
        help_level = "explain"
        goal = "understand_concept"

        # Comparison Detection (e.g., "difference between X and Y", "X vs Y")
        if any(k in normalized for k in ["difference between", "vs", "versus", "compare", "distinguish"]):
            intent = "comparison"
            visual_need = "comparison_table"
            goal = "compare_concepts"

        # Simple Definition Detection (e.g., "what is X", "define X")
        elif normalized.startswith("what is ") or normalized.startswith("define ") or normalized.startswith("meaning of "):
            intent = "definition"
            complexity = "low"
            visual_need = "none"
            goal = "define_concept"

        # Derivation / Proof Detection
        elif any(k in normalized for k in ["derive", "derivation", "evaluate", "calculate", "step by step", "prove"]):
            intent = "derivation"
            visual_need = "derivation_flow"
            help_level = "step_by_step"
            complexity = "high"
            goal = "step_by_step_derivation"

        # Mechanics Problem / Geometric Incline Detection
        elif any(k in normalized for k in ["wedge", "incline", "pulley", "block on", "free body", "fbd"]):
            intent = "problem_solving"
            visual_need = "diagram"
            complexity = "high"
            goal = "solve_physics_problem"

        # Conceptual "Why" Questions
        elif normalized.startswith("why ") or "reason behind" in normalized:
            intent = "concept_explanation"
            goal = "understand_underlying_cause"
            if any(k in normalized for k in ["wedge", "incline", "fbd"]):
                visual_need = "diagram"

        # 3. Language Detection (Hinglish check)
        hinglish_markers = {"karega", "hota", "hoti", "hai", "karo", "kyun", "kaise", "kya", "ko", "se", "par", "me"}
        has_hinglish = bool(words.intersection(hinglish_markers))
        language = "hinglish" if has_hinglish else "english"

        # 4. Key Entities Extraction
        extracted_entities = list(words.intersection(
            cls.PHYSICS_KEYWORDS | cls.CHEMISTRY_KEYWORDS | cls.MATH_KEYWORDS
        ))[:6]

        return AnalysisContext(
            intent=intent,
            subject=subject,
            complexity=complexity,
            language=language,
            requested_help_level=help_level,
            detected_visual_need=visual_need,
            key_entities=extracted_entities,
            user_goal=goal,
        )
