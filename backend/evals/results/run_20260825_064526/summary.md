# Evaluation Run Summary: `eval_run_20260825_064526`

- **Timestamp**: 2026-08-25T06:45:35.809495+00:00
- **Mode**: `live_gemini`
- **Model**: `gemini-3.5-flash`
- **Prompt Version**: `v1.0`
- **Total Cases**: 3 (Success: 0, Fail: 3)

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
| `J_SCHEMA_FAILURE` | 3 |

---

## Case-by-Case Breakdown

| Case ID | Subject | Category | Status | Latency | Nodes | Failures |
|---|---|---|---|---|---|---|
| `eval-chem-008` | chemistry | mechanism | FAIL | 2119 ms | 0 | 1 |
| `eval-math-006` | mathematics | derivation | FAIL | 4445 ms | 0 | 1 |
| `eval-phy-006` | physics | derivation | FAIL | 2252 ms | 0 | 1 |