import json
from pathlib import Path
from typing import Dict, List, Optional
from backend.evals.schemas import HumanReviewFlags, HumanReviewScorecard


RUBRIC_DIMENSIONS: Dict[str, Dict[str, str]] = {
    "factual_correctness": {
        "title": "Factual & Scientific Correctness",
        "scale_1": "Contains serious factual, mathematical, or scientific errors.",
        "scale_3": "Mostly correct with minor inaccuracies or ambiguous assumptions.",
        "scale_5": "Completely rigorous, mathematically and scientifically exact with proper units/sign conventions.",
    },
    "reasoning_continuity": {
        "title": "Step-by-Step Reasoning Continuity",
        "scale_1": "Disjoint assertions without logical transitions or justification.",
        "scale_3": "Reasonable progression with occasional algebraic or conceptual leaps.",
        "scale_5": "Flawless deductive chain; every step explains 'why' and connects to prior steps.",
    },
    "pedagogical_clarity": {
        "title": "Pedagogical Clarity & Student Empathy",
        "scale_1": "Confusing, intimidating wall of text/formulas.",
        "scale_3": "Understandable explanation suitable for a student with prior preparation.",
        "scale_5": "Crystal clear, highly intuitive explanation that builds core conceptual models effortlessly.",
    },
    "appropriate_detail": {
        "title": "Appropriate Detail & Cognitive Sizing",
        "scale_1": "Extremely bloated or dangerously superficial.",
        "scale_3": "Adequate detail, slightly verbose or slightly brief.",
        "scale_5": "Perfect cognitive sizing; addresses the question directly without irrelevant fluff.",
    },
    "visual_usefulness": {
        "title": "Visual & Structural Restraint",
        "scale_1": "Gratuitous decorative visual or missing crucial spatial diagram.",
        "scale_3": "Reasonable layout; visual is somewhat helpful.",
        "scale_5": "High visual leverage; diagram/table significantly reduces cognitive load; no decorative cards.",
    },
    "relationship_clarity": {
        "title": "Semantic Relationship Graph Quality",
        "scale_1": "Disconnected or contradictory logical edges (e.g. conclusion precedes derivation).",
        "scale_3": "Adequate linking between consecutive nodes.",
        "scale_5": "Precise, meaningful causal/derivational relationships linking equations to annotations and takeaways.",
    },
    "language_naturalness": {
        "title": "Language Naturalness (English/Hinglish)",
        "scale_1": "Robotic, unnatural, or awkward literal translations.",
        "scale_3": "Acceptable phrasing with minor stylistic awkwardness.",
        "scale_5": "Natural, fluent, and highly engaging tone tailored for Indian JEE students.",
    },
    "jee_relevance": {
        "title": "JEE Main & Advanced Pedagogical Standard",
        "scale_1": "Elementary school level or irrelevant to competitive exam demands.",
        "scale_3": "Standard textbook level coverage.",
        "scale_5": "Authentic JEE Advanced rigor, highlighting exam traps, shortcuts, and boundary conditions.",
    },
}


class ScorecardManager:
    """Manages recording and persisting human evaluation scorecards."""

    def __init__(self, storage_dir: Optional[Path] = None):
        self._dir = storage_dir or Path(__file__).resolve().parent / "results" / "scorecards"
        self._dir.mkdir(parents=True, exist_ok=True)

    def save_scorecard(self, scorecard: HumanReviewScorecard) -> Path:
        """Saves a scorecard to a JSON file."""
        file_path = self._dir / f"{scorecard.case_id}_{scorecard.reviewer}.json"
        file_path.write_text(scorecard.model_dump_json(indent=2), encoding="utf-8")
        return file_path

    def load_scorecard(self, case_id: str, reviewer: str) -> Optional[HumanReviewScorecard]:
        """Loads a scorecard from disk."""
        file_path = self._dir / f"{case_id}_{reviewer}.json"
        if not file_path.exists():
            return None
        data = json.loads(file_path.read_text(encoding="utf-8"))
        return HumanReviewScorecard.model_validate(data)

    def list_all_scorecards(self) -> List[HumanReviewScorecard]:
        """Lists all saved human scorecards."""
        results = []
        for p in self._dir.glob("*.json"):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                results.append(HumanReviewScorecard.model_validate(data))
            except Exception:
                continue
        return results
