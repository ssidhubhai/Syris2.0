import argparse
import asyncio
import json
import logging
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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

from backend.app.core.config import settings
from backend.app.providers.base import (
    BaseModelProvider,
    ModelNotCertifiedException,
    ProviderResponse,
    ProviderStructuredRequest,
    ProviderTokenUsage,
)

from backend.app.providers.google_provider import GoogleProvider
from backend.app.providers.registry import default_registry
from backend.app.schemas.ai_explanation import (
    AIExplanationDocumentSchema,
    AIExplanationNodeSchema,
    AINodeContentSchema,
    AIRelationshipSchema,
)
from backend.app.schemas.explanation import ExplanationDocumentSchema
from backend.evals.latency_tracer import LatencyTracer
from backend.evals.metrics import MetricsEvaluator
from backend.evals.schemas import (
    AutomatedMetrics,
    EvaluationCase,
    EvaluationCaseResult,
    EvaluationRunReport,
    ModelComparisonSummary,
)

logger = logging.getLogger("syris.evals")
SEED_DIR = Path(__file__).resolve().parent / "seed"
RESULTS_DIR = Path(__file__).resolve().parent / "results"


class MockEvaluationProvider(BaseModelProvider):
    """Synthetic provider generating deterministic compliant ExplanationDocuments for offline testing."""

    @property
    def provider_name(self) -> str:
        return "mock_eval_provider"

    async def generate_structured(self, request: ProviderStructuredRequest) -> ProviderResponse:
        await asyncio.sleep(0.01)  # Simulate fast local processing
        
        # Build synthetic compliant response based on query
        title = "Evaluation Mock Response"
        nodes = [
            AIExplanationNodeSchema(
                id="node-head-1",
                type="heading",
                content=AINodeContentSchema(text=f"Explanation: {request.prompt[:40]}...", level=1),
                importance="critical",
            ),
            AIExplanationNodeSchema(
                id="node-def-1",
                type="definition",
                content=AINodeContentSchema(
                    title="Key Definition",
                    latex="E = mc^2",
                    annotation="Fundamental principle for the problem.",
                ),
                importance="critical",
            ),
            AIExplanationNodeSchema(
                id="node-txt-1",
                type="text",
                content=AINodeContentSchema(
                    markdown="Detailed physical intuition and boundary condition analysis.",
                ),
                importance="supporting",
            ),
            AIExplanationNodeSchema(
                id="node-conc-1",
                type="conclusion",
                content=AINodeContentSchema(
                    title="Takeaway Summary",
                    latex="\\Delta U = q + w",
                    highlight=True,
                ),
                importance="critical",
            ),
        ]
        rels = [
            AIRelationshipSchema(
                **{"from": "node-head-1", "to": "node-def-1", "type": "defines", "label": "defines core"}
            ),
            AIRelationshipSchema(
                **{"from": "node-def-1", "to": "node-conc-1", "type": "explains", "label": "leads to"}
            ),
        ]

        mock_doc = AIExplanationDocumentSchema(
            document_id=f"doc-mock-{uuid.uuid4().hex[:8]}",
            session_id=request.request_id,
            title=title,
            intent="concept_explanation",
            subject="physics",
            language="english",
            nodes=nodes,
            relationships=rels,
        )

        return ProviderResponse(
            request_id=request.request_id,
            model_id=request.model_id,
            provider="mock",
            raw_text="{}",
            structured_output=mock_doc,
            latency_ms=10,
            token_usage=ProviderTokenUsage(input_tokens=150, output_tokens=220, total_tokens=370),
        )

    async def generate_text(self, request: Any) -> ProviderResponse:
        return ProviderResponse(
            request_id=request.request_id,
            model_id=request.model_id,
            provider="mock",
            text="Mock text response",
            latency_ms=10,
        )

    async def list_models(self) -> List[Any]:
        return []

    async def get_model(self, model_id: str) -> Any:
        return None

    async def health_check(self) -> Any:
        return None




class EvaluationDatasetLoader:
    """Loads and filters curated evaluation cases from JSON seed files."""

    @classmethod
    def load_all_cases(cls) -> List[EvaluationCase]:
        cases: List[EvaluationCase] = []
        for file_path in sorted(SEED_DIR.glob("*.json")):
            try:
                data = json.loads(file_path.read_text(encoding="utf-8"))
                for item in data:
                    cases.append(EvaluationCase.model_validate(item))
            except Exception as e:
                logger.error(f"Failed to load seed file '{file_path.name}': {e}")
                raise
        return cases

    @classmethod
    def filter_cases(
        cls,
        cases: List[EvaluationCase],
        ids: Optional[List[str]] = None,
        subject: Optional[str] = None,
        category: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[EvaluationCase]:
        filtered = cases
        if ids:
            id_set = set(ids)
            filtered = [c for c in filtered if c.id in id_set]
        if subject:
            filtered = [c for c in filtered if c.subject == subject]
        if category:
            filtered = [c for c in filtered if c.category == category]
        if limit and limit > 0:
            filtered = filtered[:limit]
        return filtered


class EvaluationRunner:
    """Executes evaluation suite, records latency, computes metrics, and produces reports."""

    def __init__(
        self,
        mode: str = "mock",
        model_id: str = "gemini-3.5-flash-lite",
        output_dir: Optional[Path] = None,
    ):
        self.mode = mode
        self.model_id = model_id
        self.output_dir = output_dir or RESULTS_DIR / f"run_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if mode == "live_gemini":
            # Model certification gate: reject uncertified models immediately
            default_registry.validate_eligibility(model_id, required_status="CERTIFIED_FOR_DEV")
            self.provider: BaseModelProvider = GoogleProvider()
        else:
            self.provider = MockEvaluationProvider()

        self.generator = ExplanationGenerator(
            provider=self.provider,
            default_model=self.model_id,
        )

    async def run_case(self, case: EvaluationCase) -> EvaluationCaseResult:
        """Evaluates a single case with fine-grained latency tracing."""
        tracer = LatencyTracer()
        request_id = f"eval-{case.id}-{int(datetime.now(timezone.utc).timestamp())}"
        session_id = f"sess-eval-{uuid.uuid4().hex[:8]}"

        doc: Optional[ExplanationDocumentSchema] = None
        error_msg: Optional[str] = None
        token_dict: Dict[str, int] = {}

        try:
            doc, provider_resp = await self.generator.generate_explanation(
                query=case.question,
                session_id=session_id,
                request_id=request_id,
                model_id=self.model_id,
                tracer=tracer,
            )
            if provider_resp.token_usage:
                token_dict = {
                    "input_tokens": provider_resp.token_usage.input_tokens,
                    "output_tokens": provider_resp.token_usage.output_tokens,
                    "total_tokens": provider_resp.token_usage.total_tokens,
                }
        except Exception as e:
            error_msg = str(e)
            logger.warning(f"[EVAL_CASE_FAIL] case={case.id} error={error_msg}")

        tracer.finish_total()
        breakdown = tracer.to_breakdown()

        metrics, failures = MetricsEvaluator.evaluate(
            case=case,
            doc=doc,
            latency_breakdown=breakdown,
            raw_error=error_msg,
            token_usage=token_dict,
        )

        doc_dump = doc.model_dump(by_alias=True) if doc else None

        return EvaluationCaseResult(
            case_id=case.id,
            subject=case.subject,
            category=case.category,
            question=case.question,
            model_id=self.model_id,
            prompt_version=self.generator.prompt_version,
            success=(doc is not None and error_msg is None and metrics.structural.schema_valid),
            error_message=error_msg,
            document=doc_dump,
            metrics=metrics,
            failures=failures,
        )

    async def run_suite(self, cases: List[EvaluationCase]) -> EvaluationRunReport:
        """Runs the entire filtered suite and generates summary artifacts."""
        run_id = f"eval_run_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
        case_results: List[EvaluationCaseResult] = []
        failure_dist: Dict[str, int] = {}

        print(f"\n============================================================")
        print(f"STARTING EVALUATION RUN: {run_id}")
        print(f"Mode: {self.mode.upper()} | Model: {self.model_id} | Prompt: {self.generator.prompt_version}")
        print(f"Total Cases: {len(cases)}")
        print(f"============================================================\n")

        for idx, case in enumerate(cases, 1):
            print(f"[{idx:02d}/{len(cases):02d}] Evaluating {case.id} ({case.subject}/{case.category})... ", end="", flush=True)
            res = await self.run_case(case)
            case_results.append(res)

            status = "PASS" if res.success else "FAIL"
            latency = int(res.metrics.reliability.total_latency_ms)
            nodes = res.metrics.complexity.node_count
            print(f"[{status}] in {latency}ms (nodes={nodes}, failures={len(res.failures)})")

            for f in res.failures:
                failure_dist[f.category_code] = failure_dist.get(f.category_code, 0) + 1

        successful = sum(1 for r in case_results if r.success)
        failed = len(case_results) - successful

        # Latency summary
        latencies = [r.metrics.reliability.total_latency_ms for r in case_results if r.success]
        gemini_calls = [r.metrics.latency_breakdown.gemini_request_time_ms for r in case_results if r.success]
        prep_calls = [r.metrics.latency_breakdown.preprocessing_time_ms for r in case_results if r.success]

        latency_summary = {
            "avg_total_ms": round(sum(latencies) / len(latencies), 2) if latencies else 0.0,
            "avg_gemini_request_ms": round(sum(gemini_calls) / len(gemini_calls), 2) if gemini_calls else 0.0,
            "avg_preprocessing_ms": round(sum(prep_calls) / len(prep_calls), 2) if prep_calls else 0.0,
        }

        # Model summary
        model_summary = ModelComparisonSummary(
            model_id=self.model_id,
            total_cases=len(cases),
            success_count=successful,
            failure_count=failed,
            avg_latency_ms=latency_summary["avg_total_ms"],
            avg_node_count=round(sum(r.metrics.complexity.node_count for r in case_results) / len(cases), 2) if cases else 0,
            avg_relationship_count=round(sum(r.metrics.complexity.relationship_count for r in case_results) / len(cases), 2) if cases else 0,
            avg_concept_coverage_rate=round(sum(r.metrics.concept_signal.concept_coverage_rate for r in case_results) / len(cases), 2) if cases else 0,
            unnecessary_visual_count=sum(1 for r in case_results if r.metrics.presentation.unnecessary_visual_signal),
            missing_visual_count=sum(1 for r in case_results if r.metrics.presentation.missing_visual_signal),
            critical_error_count=sum(1 for r in case_results if any(f.category_code == "B_INCORRECT_REASONING" for f in r.failures)),
        )

        report = EvaluationRunReport(
            run_id=run_id,
            mode=self.mode,  # type: ignore[arg-type]
            model_ids=[self.model_id],
            prompt_version=self.generator.prompt_version,
            total_cases_evaluated=len(cases),
            successful_cases=successful,
            failed_cases=failed,
            case_results=case_results,
            model_summaries=[model_summary],
            latency_summary=latency_summary,
            failure_distribution=failure_dist,
        )

        self._persist_artifacts(report)
        return report

    def _persist_artifacts(self, report: EvaluationRunReport) -> None:
        """Writes JSON report and Markdown summary to output directory."""
        # 1. Save JSON artifact
        json_path = self.output_dir / "results.json"
        json_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")

        # 2. Save Markdown summary
        md_path = self.output_dir / "summary.md"
        md_content = self._build_markdown_summary(report)
        md_path.write_text(md_content, encoding="utf-8")

        # 3. Save digital paper samples for visual inspection
        samples_dir = self.output_dir / "digital_paper_samples"
        samples_dir.mkdir(parents=True, exist_ok=True)
        for res in report.case_results:
            if res.document:
                doc_path = samples_dir / f"{res.case_id}.json"
                doc_path.write_text(json.dumps(res.document, indent=2), encoding="utf-8")

        print(f"\nArtifacts successfully written to: {self.output_dir}")
        print(f"- Results JSON: {json_path}")
        print(f"- Summary Markdown: {md_path}")

    def _build_markdown_summary(self, report: EvaluationRunReport) -> str:
        lines = [
            f"# Evaluation Run Summary: `{report.run_id}`",
            f"",
            f"- **Timestamp**: {report.timestamp.isoformat()}",
            f"- **Mode**: `{report.mode}`",
            f"- **Model**: `{report.model_ids[0]}`",
            f"- **Prompt Version**: `{report.prompt_version}`",
            f"- **Total Cases**: {report.total_cases_evaluated} (Success: {report.successful_cases}, Fail: {report.failed_cases})",
            f"",
            f"---",
            f"",
            f"## Latency Breakdown Summary",
            f"",
            f"| Metric | Duration (ms) | % of Total |",
            f"|---|---|---|",
        ]
        avg_total = report.latency_summary.get("avg_total_ms", 1.0) or 1.0
        avg_llm = report.latency_summary.get("avg_gemini_request_ms", 0.0)
        avg_prep = report.latency_summary.get("avg_preprocessing_ms", 0.0)
        llm_pct = round((avg_llm / avg_total) * 100, 1)
        prep_pct = round((avg_prep / avg_total) * 100, 1)

        lines.extend([
            f"| **Deterministic Preprocessing** | {avg_prep:.2f} ms | {prep_pct}% |",
            f"| **Gemini Structured Call** | {avg_llm:.2f} ms | {llm_pct}% |",
            f"| **Average Total Pipeline** | {avg_total:.2f} ms | 100.0% |",
            f"",
            f"---",
            f"",
            f"## Failure Distribution (Taxonomy A–J)",
            f"",
            f"| Category Code | Failure Count |",
            f"|---|---|",
        ])
        for code, cnt in sorted(report.failure_distribution.items()):
            lines.append(f"| `{code}` | {cnt} |")

        lines.extend([
            f"",
            f"---",
            f"",
            f"## Case-by-Case Breakdown",
            f"",
            f"| Case ID | Subject | Category | Status | Latency | Nodes | Failures |",
            f"|---|---|---|---|---|---|---|",
        ])
        for r in report.case_results:
            status = "PASS" if r.success else "FAIL"
            latency = f"{int(r.metrics.reliability.total_latency_ms)} ms"
            nodes = r.metrics.complexity.node_count
            fails = len(r.failures)
            lines.append(f"| `{r.case_id}` | {r.subject} | {r.category} | {status} | {latency} | {nodes} | {fails} |")

        return "\n".join(lines)


async def main_cli():
    parser = argparse.ArgumentParser(description="Syris 2.0 Evaluation & Quality Runner (Phase 4B)")
    parser.add_argument("--mock", action="store_true", default=False, help="Run in mock mode (fast, no API calls)")
    parser.add_argument("--live-gemini", action="store_true", default=False, help="Opt-in flag for live Gemini API calls")
    parser.add_argument("--model", type=str, default="gemini-3.5-flash-lite", help="Target model ID")
    parser.add_argument("--ids", type=str, default=None, help="Comma-separated case IDs to evaluate (e.g. eval-phy-001,eval-chem-001)")
    parser.add_argument("--subject", type=str, default=None, help="Filter by subject (physics, chemistry, mathematics)")
    parser.add_argument("--category", type=str, default=None, help="Filter by category (conceptual, derivation, diagram, comparison, hinglish, compact)")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of cases to evaluate")
    parser.add_argument("--compare-models", type=str, default=None, help="Comma-separated model IDs to benchmark comparatively")
    parser.add_argument("--output-dir", type=str, default=None, help="Custom output directory")

    args = parser.parse_args()

    mode = "live_gemini" if args.live_gemini else "mock"
    all_cases = EvaluationDatasetLoader.load_all_cases()
    
    ids_filter = [i.strip() for i in args.ids.split(",")] if args.ids else None
    selected_cases = EvaluationDatasetLoader.filter_cases(
        cases=all_cases,
        ids=ids_filter,
        subject=args.subject,
        category=args.category,
        limit=args.limit,
    )

    if not selected_cases:
        print("No cases matched the specified criteria.")
        sys.exit(1)

    out_dir = Path(args.output_dir) if args.output_dir else None

    if args.compare_models:
        models = [m.strip() for m in args.compare_models.split(",")]
        print(f"Executing comparative evaluation across models: {models}")
        for mid in models:
            runner = EvaluationRunner(mode=mode, model_id=mid, output_dir=out_dir)
            await runner.run_suite(selected_cases)
    else:
        runner = EvaluationRunner(mode=mode, model_id=args.model, output_dir=out_dir)
        await runner.run_suite(selected_cases)


if __name__ == "__main__":
    asyncio.run(main_cli())
