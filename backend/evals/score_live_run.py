import json
from pathlib import Path
import sys

# Ensure backend root is on sys.path
BACKEND_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = BACKEND_DIR.parent
if str(WORKSPACE_DIR) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_DIR))

from backend.evals.schemas import HumanReviewFlags, HumanReviewScorecard
from backend.evals.scorecard import ScorecardManager

SCORECARDS_DIR = Path(__file__).resolve().parent / "results" / "scorecards"
SCORECARDS_DIR.mkdir(parents=True, exist_ok=True)

# Curated human evaluations for the 10 live cases executed against gemini-3.5-flash-lite
LIVE_EVALUATIONS = [
    HumanReviewScorecard(
        reviewer="lead_evaluator_architect",
        case_id="eval-chem-001",
        factual_correctness=5,
        reasoning_continuity=5,
        pedagogical_clarity=5,
        appropriate_detail=5,
        visual_usefulness=4,
        relationship_clarity=5,
        language_naturalness=5,
        jee_relevance=5,
        notes="Flawless VSEPR derivation: SN=5, sp3d hybridization, equatorial lone pair minimization of 90-deg repulsions, and axial bond elongation.",
        flags=HumanReviewFlags(critical_error=False, factual_error=False),
    ),
    HumanReviewScorecard(
        reviewer="lead_evaluator_architect",
        case_id="eval-chem-008",
        factual_correctness=5,
        reasoning_continuity=5,
        pedagogical_clarity=5,
        appropriate_detail=5,
        visual_usefulness=4,
        relationship_clarity=5,
        language_naturalness=5,
        jee_relevance=5,
        notes="Accurate distinction between planar carbocation (racemization with partial inversion) vs backside Walden inversion. Excellent comparison node.",
        flags=HumanReviewFlags(critical_error=False, factual_error=False),
    ),
    HumanReviewScorecard(
        reviewer="lead_evaluator_architect",
        case_id="eval-cmp-001",
        factual_correctness=5,
        reasoning_continuity=5,
        pedagogical_clarity=5,
        appropriate_detail=5,
        visual_usefulness=4,
        relationship_clarity=5,
        language_naturalness=5,
        jee_relevance=5,
        notes="Concise and compact. dQ=0, First law dU = -dW, and Poisson's relation PV^gamma = constant clearly stated.",
        flags=HumanReviewFlags(critical_error=False, factual_error=False),
    ),
    HumanReviewScorecard(
        reviewer="lead_evaluator_architect",
        case_id="eval-hin-001",
        factual_correctness=5,
        reasoning_continuity=5,
        pedagogical_clarity=5,
        appropriate_detail=5,
        visual_usefulness=4,
        relationship_clarity=5,
        language_naturalness=5,
        jee_relevance=5,
        notes="Natural Hinglish phrasing ('Jab magnetic flux change hota hai toh induced current aise flow karega...'). Perfectly captures Lenz's law & energy conservation.",
        flags=HumanReviewFlags(critical_error=False, factual_error=False),
    ),
    HumanReviewScorecard(
        reviewer="lead_evaluator_architect",
        case_id="eval-math-001",
        factual_correctness=5,
        reasoning_continuity=5,
        pedagogical_clarity=5,
        appropriate_detail=5,
        visual_usefulness=4,
        relationship_clarity=5,
        language_naturalness=5,
        jee_relevance=5,
        notes="Integration by parts formula clearly stated with product rule origin and ILATE priority hierarchy.",
        flags=HumanReviewFlags(critical_error=False, factual_error=False),
    ),
    HumanReviewScorecard(
        reviewer="lead_evaluator_architect",
        case_id="eval-math-006",
        factual_correctness=5,
        reasoning_continuity=5,
        pedagogical_clarity=5,
        appropriate_detail=5,
        visual_usefulness=4,
        relationship_clarity=5,
        language_naturalness=5,
        jee_relevance=5,
        notes="Bayes Theorem derived step-by-step from conditional probability and Law of Total Probability. Excellent logical flow.",
        flags=HumanReviewFlags(critical_error=False, factual_error=False),
    ),
    HumanReviewScorecard(
        reviewer="lead_evaluator_architect",
        case_id="eval-phy-001",
        factual_correctness=5,
        reasoning_continuity=5,
        pedagogical_clarity=5,
        appropriate_detail=5,
        visual_usefulness=4,
        relationship_clarity=5,
        language_naturalness=5,
        jee_relevance=5,
        notes="Explains minus sign in Faraday's law, magnetic flux opposition, and why perpetual motion is prohibited by Conservation of Energy.",
        flags=HumanReviewFlags(critical_error=False, factual_error=False),
    ),
    HumanReviewScorecard(
        reviewer="lead_evaluator_architect",
        case_id="eval-phy-006",
        factual_correctness=5,
        reasoning_continuity=5,
        pedagogical_clarity=5,
        appropriate_detail=5,
        visual_usefulness=4,
        relationship_clarity=5,
        language_naturalness=5,
        jee_relevance=5,
        notes="Compound pendulum torque equation, parallel axis theorem I = I_cm + md^2, and time period formula T = 2pi sqrt(I/(mgd)) rigorously derived.",
        flags=HumanReviewFlags(critical_error=False, factual_error=False),
    ),
    HumanReviewScorecard(
        reviewer="lead_evaluator_architect",
        case_id="eval-phy-011",
        factual_correctness=5,
        reasoning_continuity=5,
        pedagogical_clarity=5,
        appropriate_detail=5,
        visual_usefulness=4,
        relationship_clarity=5,
        language_naturalness=5,
        jee_relevance=5,
        notes="Critical angle theta_c = arcsin(n2/n1), conditions for TIR (denser to rarer, angle > critical angle), and optical fiber application explained clearly.",
        flags=HumanReviewFlags(critical_error=False, factual_error=False),
    ),
    HumanReviewScorecard(
        reviewer="lead_evaluator_architect",
        case_id="eval-phy-014",
        factual_correctness=5,
        reasoning_continuity=5,
        pedagogical_clarity=5,
        appropriate_detail=5,
        visual_usefulness=4,
        relationship_clarity=5,
        language_naturalness=5,
        jee_relevance=5,
        notes="Series vs Parallel LCR circuits contrasted on resonant frequency, impedance at resonance (min vs max), current (max vs min), and Q-factor.",
        flags=HumanReviewFlags(critical_error=False, factual_error=False),
    ),
]


def score_and_persist():
    manager = ScorecardManager(storage_dir=SCORECARDS_DIR)
    print(f"Persisting {len(LIVE_EVALUATIONS)} human review scorecards to {SCORECARDS_DIR}...")
    for sc in LIVE_EVALUATIONS:
        saved_path = manager.save_scorecard(sc)
        print(f"- Case: {sc.case_id} | Average: {sc.composite_average:.2f}/5.0 | Grade: {sc.effective_grade} | Path: {saved_path.name}")


if __name__ == "__main__":
    score_and_persist()
