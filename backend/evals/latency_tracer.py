import time
from typing import Dict, Optional
from backend.evals.schemas import LatencyBreakdown


class LatencyTracer:
    """
    High-resolution monotonic timer for measuring individual pipeline stages.
    Tracks wall-clock milliseconds across preprocessing, prompt prep, LLM request,
    parsing, validation, persistence, and total roundtrip.
    """

    def __init__(self):
        self._timestamps: Dict[str, float] = {}
        self._stage_durations_ms: Dict[str, float] = {}
        self._start_time: float = time.perf_counter()

    def start_stage(self, stage_name: str) -> None:
        """Marks the start of a timed stage."""
        self._timestamps[stage_name] = time.perf_counter()

    def end_stage(self, stage_name: str) -> float:
        """Marks the end of a timed stage and returns duration in ms."""
        start = self._timestamps.get(stage_name)
        if start is None:
            return 0.0
        duration_ms = round((time.perf_counter() - start) * 1000.0, 2)
        self._stage_durations_ms[stage_name] = duration_ms
        return duration_ms

    def record_direct(self, stage_name: str, duration_ms: float) -> None:
        """Directly records a measured duration."""
        self._stage_durations_ms[stage_name] = round(duration_ms, 2)

    def finish_total(self) -> float:
        """Calculates total elapsed time since tracer instantiation."""
        total_ms = round((time.perf_counter() - self._start_time) * 1000.0, 2)
        self._stage_durations_ms["total_pipeline"] = total_ms
        return total_ms

    def to_breakdown(self) -> LatencyBreakdown:
        """Exports the recorded stages into a LatencyBreakdown schema."""
        return LatencyBreakdown(
            preprocessing_time_ms=self._stage_durations_ms.get("preprocessing", 0.0),
            prompt_prep_time_ms=self._stage_durations_ms.get("prompt_prep", 0.0),
            gemini_request_time_ms=self._stage_durations_ms.get("gemini_request", 0.0),
            response_parse_time_ms=self._stage_durations_ms.get("response_parse", 0.0),
            validation_time_ms=self._stage_durations_ms.get("validation", 0.0),
            persistence_time_ms=self._stage_durations_ms.get("persistence", 0.0),
            total_pipeline_time_ms=self._stage_durations_ms.get("total_pipeline", 0.0),
        )

    def summary_dict(self) -> Dict[str, float]:
        """Returns key-value mapping of all measured stages."""
        return dict(self._stage_durations_ms)
