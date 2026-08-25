# Evaluation Run Summary: `eval_run_20260825_061949`

- **Timestamp**: 2026-08-25T06:19:49.609133+00:00
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
| `eval-chem-001` | chemistry | conceptual | FAIL | 106 ms | 0 | 1 |
| `eval-chem-008` | chemistry | mechanism | FAIL | 0 ms | 0 | 1 |
| `eval-cmp-001` | physics | compact | FAIL | 0 ms | 0 | 1 |
| `eval-hin-001` | physics | hinglish | FAIL | 0 ms | 0 | 1 |
| `eval-math-001` | mathematics | conceptual | FAIL | 0 ms | 0 | 1 |
| `eval-math-006` | mathematics | derivation | FAIL | 0 ms | 0 | 1 |
| `eval-phy-001` | physics | conceptual | FAIL | 1 ms | 0 | 1 |
| `eval-phy-006` | physics | derivation | FAIL | 1 ms | 0 | 1 |
| `eval-phy-011` | physics | diagram | FAIL | 0 ms | 0 | 1 |
| `eval-phy-014` | physics | comparison | FAIL | 0 ms | 0 | 1 |