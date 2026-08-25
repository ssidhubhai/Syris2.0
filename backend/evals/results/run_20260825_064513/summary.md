# Evaluation Run Summary: `eval_run_20260825_064513`

- **Timestamp**: 2026-08-25T06:45:26.912463+00:00
- **Mode**: `live_gemini`
- **Model**: `gemini-3.5-flash-lite`
- **Prompt Version**: `v1.0`
- **Total Cases**: 3 (Success: 3, Fail: 0)

---

## Latency Breakdown Summary

| Metric | Duration (ms) | % of Total |
|---|---|---|
| **Deterministic Preprocessing** | 0.38 ms | 0.0% |
| **Gemini Structured Call** | 4396.04 ms | 100.0% |
| **Average Total Pipeline** | 4397.79 ms | 100.0% |

---

## Failure Distribution (Taxonomy A–J)

| Category Code | Failure Count |
|---|---|

---

## Case-by-Case Breakdown

| Case ID | Subject | Category | Status | Latency | Nodes | Failures |
|---|---|---|---|---|---|---|
| `eval-chem-008` | chemistry | mechanism | PASS | 4629 ms | 5 | 0 |
| `eval-math-006` | mathematics | derivation | PASS | 4759 ms | 10 | 0 |
| `eval-phy-006` | physics | derivation | PASS | 3804 ms | 7 | 0 |