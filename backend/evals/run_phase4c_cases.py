import asyncio
import json
import logging
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

# Ensure backend root is on sys.path
BACKEND_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = BACKEND_DIR.parent
if str(WORKSPACE_DIR) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_DIR))

try:
    from dotenv import load_dotenv
    load_dotenv(BACKEND_DIR / ".env")
except ImportError:
    pass

from backend.app.ai.explanation_generator import ExplanationGenerator
from backend.app.providers.google_provider import GoogleProvider
from backend.app.providers.registry import default_registry
from backend.evals.latency_tracer import LatencyTracer

logger = logging.getLogger("syris.phase4c")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

OUTPUT_DIR = BACKEND_DIR / "evals" / "results" / "phase4c_live"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PHASE4C_CASES = [
    {
        "case_id": "case-1-compact",
        "title": "Centripetal Acceleration Definition",
        "subject": "physics",
        "category": "compact",
        "query": "What is centripetal acceleration? Define it and state its magnitude and directional relationship with velocity vector.",
    },
    {
        "case_id": "case-2-concept-friction",
        "title": "Microscopic Origin of Relative Friction",
        "subject": "physics",
        "category": "conceptual",
        "query": "Why does friction oppose the tendency of relative motion rather than absolute motion? Explain microscopic interlocking and relative velocity.",
    },
    {
        "case_id": "case-3-chem-sn1-sn2",
        "title": "SN1 vs SN2 Mechanisms Comparison",
        "subject": "chemistry",
        "category": "comparison",
        "query": "What is the difference between SN1 and SN2 reaction mechanisms in organic chemistry? Compare kinetics, intermediate, solvent, and stereochemistry.",
    },
    {
        "case_id": "case-4-phy-pendulum",
        "title": "Simple Pendulum Time Period Derivation",
        "subject": "physics",
        "category": "derivation",
        "query": "Derive the time period formula T = 2\\pi\\sqrt{L/g} of a simple pendulum for small angular displacements using the restoring torque equation.",
    },
    {
        "case_id": "case-5-math-by-parts",
        "title": "Integration by Parts Formula Derivation",
        "subject": "mathematics",
        "category": "derivation",
        "query": "Derive the integration by parts formula \\int u \\, dv = uv - \\int v \\, du starting from the product rule of differentiation.",
    },
    {
        "case_id": "case-6-hinglish-lift",
        "title": "Apparent Weight in Accelerating Lift (Hinglish)",
        "subject": "physics",
        "category": "hinglish",
        "query": "Bhai mechanics me jab lift upward accelerate hoti hai toh apparent weight kyu increase hota hai? Normal reaction aur pseudo force se samjhao.",
    },
    {
        "case_id": "case-7-optics-tir",
        "title": "Total Internal Reflection & Critical Angle",
        "subject": "physics",
        "category": "optics_spatial",
        "query": "Explain Total Internal Reflection (TIR) at a denser-to-rarer medium interface and derive the critical angle condition \\sin \\theta_c = 1/n.",
    },
    {
        "case_id": "case-8-physics-wedge",
        "title": "Block on Accelerating Wedge Problem",
        "subject": "physics",
        "category": "advanced_mixed",
        "query": "A block of mass m is placed on a smooth triangular wedge of mass M and inclination \\theta. The wedge is accelerated horizontally with acceleration a such that the block remains stationary relative to the wedge. Find a and the normal force on the block.",
    },
]


async def run_phase4c_generation():
    model_id = "gemini-3.5-flash-lite"
    default_registry.validate_eligibility(model_id, required_status="CERTIFIED_FOR_DEV")

    provider = GoogleProvider()
    generator = ExplanationGenerator(provider=provider, default_model=model_id)

    print(f"\n============================================================")
    print(f"PHASE 4C LIVE CASE GENERATION")
    print(f"Model: {model_id} | Prompt Version: {generator.prompt_version}")
    print(f"Total Target Cases: {len(PHASE4C_CASES)}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"============================================================\n")

    results_summary: List[Dict[str, Any]] = []

    for idx, case in enumerate(PHASE4C_CASES, 1):
        case_id = case["case_id"]
        query = case["query"]
        req_id = f"phase4c-{case_id}-{int(datetime.now(timezone.utc).timestamp())}"
        session_id = f"sess-p4c-{uuid.uuid4().hex[:8]}"

        print(f"[{idx:02d}/08] Generating {case_id} ({case['category']})... ", end="", flush=True)

        tracer = LatencyTracer()
        doc = None
        error_msg = None
        resp_obj = None

        try:
            doc, resp_obj = await generator.generate_explanation(
                query=query,
                session_id=session_id,
                request_id=req_id,
                model_id=model_id,
                tracer=tracer,
            )
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed {case_id}: {e}", exc_info=True)

        tracer.finish_total()
        breakdown = tracer.to_breakdown()
        total_ms = round(breakdown.total_pipeline_time_ms, 2)
        status = "PASS" if doc and not error_msg else "FAIL"

        node_count = len(doc.nodes) if doc else 0
        rel_count = len(doc.relationships) if doc else 0

        print(f"[{status}] in {total_ms}ms (nodes={node_count}, rels={rel_count})")

        case_record = {
            "case_id": case_id,
            "title": case["title"],
            "subject": case["subject"],
            "category": case["category"],
            "query": query,
            "model_id": model_id,
            "prompt_version": generator.prompt_version,
            "status": status,
            "error_message": error_msg,
            "token_usage": {
                "input_tokens": resp_obj.token_usage.input_tokens if resp_obj and resp_obj.token_usage else 0,
                "output_tokens": resp_obj.token_usage.output_tokens if resp_obj and resp_obj.token_usage else 0,
                "total_tokens": resp_obj.token_usage.total_tokens if resp_obj and resp_obj.token_usage else 0,
            },
            "latency_breakdown": breakdown.model_dump(),
            "document": doc.model_dump(by_alias=True) if doc else None,
        }

        # Save individual case JSON
        case_file = OUTPUT_DIR / f"{case_id}.json"
        case_file.write_text(json.dumps(case_record, indent=2), encoding="utf-8")
        results_summary.append(case_record)

    # Save complete run summary
    summary_file = OUTPUT_DIR / "phase4c_summary.json"
    summary_file.write_text(json.dumps(results_summary, indent=2), encoding="utf-8")

    print(f"\nAll 8 Phase 4C cases saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(run_phase4c_generation())
