# Evaluation Run Summary: `eval_run_20260825_063735`

- **Timestamp**: 2026-08-25T06:38:30.028573+00:00
- **Mode**: `live_gemini`
- **Model**: `gemini-3.5-flash-lite`
- **Prompt Version**: `v1.0`
- **Total Cases**: 10 (Success: 0, Fail: 10)

---

## Latency Breakdown Summary

| Metric | Duration (ms) | % of Total |
|---|---|---|
| **Deterministic Preprocessing** | 0.00 ms | 0.0% |
| **Gemini Structured Call** | 0.00 ms | 0.0% |
| **Average Total Pipeline** | 1.00 ms | 100.0% |

---

## Failure Distribution (Taxonomy A–J)

| Category Code | Failure Count |
|---|---|
| `J_SCHEMA_FAILURE` | 10 |

---

## Case-by-Case Breakdown

| Case ID | Subject | Category | Status | Latency | Nodes | Failures |
|---|---|---|---|---|---|---|
| `eval-chem-001` | chemistry | conceptual | FAIL | 7081 ms | 0 | 1 |
| `eval-chem-008` | chemistry | mechanism | FAIL | 4413 ms | 0 | 1 |
| `eval-cmp-001` | physics | compact | FAIL | 3662 ms | 0 | 1 |
| `eval-hin-001` | physics | hinglish | FAIL | 4286 ms | 0 | 1 |
| `eval-math-001` | mathematics | conceptual | FAIL | 4795 ms | 0 | 1 |
| `eval-math-006` | mathematics | derivation | FAIL | 13842 ms | 0 | 1 |
| `eval-phy-001` | physics | conceptual | FAIL | 4168 ms | 0 | 1 |
| `eval-phy-006` | physics | derivation | FAIL | 3550 ms | 0 | 1 |
| `eval-phy-011` | physics | diagram | FAIL | 5383 ms | 0 | 1 |
| `eval-phy-014` | physics | comparison | FAIL | 2965 ms | 0 | 1 |