from typing import Dict, List, Optional
from backend.evals.schemas import CaseFailureItem, FailureCode


FAILURE_DEFINITIONS: Dict[FailureCode, Dict[str, str]] = {
    "A_BAD_PRESENTATION": {
        "title": "Correct but Badly Presented",
        "description": "Factual logic is sound, but presentation is cluttered, awkwardly structured, or lacks visual-conceptual balance.",
    },
    "B_INCORRECT_REASONING": {
        "title": "Incorrect Reasoning or Mathematical Error",
        "description": "Contains invalid equations, sign errors, wrong boundary assumptions, or physically impossible claims.",
    },
    "C_MISSING_CONCEPT": {
        "title": "Missing Essential Concept",
        "description": "Omits core pedagogical principles or prerequisite assumptions required for complete JEE understanding.",
    },
    "D_UNNECESSARY_VISUAL": {
        "title": "Unnecessary / Decorative Visual Generated",
        "description": "Generated a diagram or visual card when none was requested or pedagogically helpful, increasing clutter.",
    },
    "E_MISSING_USEFUL_VISUAL": {
        "title": "Missing Useful Visual",
        "description": "Omitted a diagram or coordinate representation for a spatial, geometric, or ray-tracing problem where a visual reduces cognitive load.",
    },
    "F_BROKEN_RELATIONSHIPS": {
        "title": "Broken or Misleading Semantic Graph",
        "description": "Contains dangling node references, circular loops, or illogical causal links (e.g. conclusion precedes premise).",
    },
    "G_TOO_VERBOSE": {
        "title": "Overly Verbose / Cognitive Overload",
        "description": "Exceeds reasonable length with redundant filler text, repeating formulas or conversational preambles.",
    },
    "H_TOO_TERSE": {
        "title": "Overly Terse / Insufficient Depth",
        "description": "Answers superficially without step-by-step reasoning or necessary boundary explanations.",
    },
    "I_AWKWARD_LANGUAGE": {
        "title": "Awkward or Robotic Phrasing",
        "description": "Uses unnatural English phrasing or stiff, broken Hinglish that degrades pedagogical clarity.",
    },
    "J_SCHEMA_FAILURE": {
        "title": "Schema or Technical Generation Failure",
        "description": "Failed Pydantic schema validation, returned malformed JSON, or failed backend integrity checks.",
    },
}


def make_failure_item(
    category_code: FailureCode,
    custom_description: Optional[str] = None,
) -> CaseFailureItem:
    """Helper to construct a standardized CaseFailureItem."""
    defn = FAILURE_DEFINITIONS.get(
        category_code,
        {"title": category_code, "description": "Unclassified failure mode."},
    )
    return CaseFailureItem(
        category_code=category_code,
        title=defn["title"],
        description=custom_description or defn["description"],
    )
