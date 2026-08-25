# Evaluation Run Summary: `eval_run_20260825_064005`

- **Timestamp**: 2026-08-25T06:40:55.563303+00:00
- **Mode**: `live_gemini`
- **Model**: `gemini-3.5-flash-lite`
- **Prompt Version**: `v1.0`
- **Total Cases**: 10 (Success: 8, Fail: 2)

---

## Latency Breakdown Summary

| Metric | Duration (ms) | % of Total |
|---|---|---|
| **Deterministic Preprocessing** | 0.45 ms | 0.0% |
| **Gemini Structured Call** | 5071.61 ms | 100.0% |
| **Average Total Pipeline** | 5073.43 ms | 100.0% |

---

## Failure Distribution (Taxonomy A–J)

| Category Code | Failure Count |
|---|---|
| `B_INCORRECT_REASONING` | 5 |
| `E_MISSING_USEFUL_VISUAL` | 1 |
| `J_SCHEMA_FAILURE` | 2 |

---

## Case-by-Case Breakdown

| Case ID | Subject | Category | Status | Latency | Nodes | Failures |
|---|---|---|---|---|---|---|
| `eval-chem-001` | chemistry | conceptual | PASS | 4952 ms | 6 | 0 |
| `eval-chem-008` | chemistry | mechanism | PASS | 4143 ms | 5 | 0 |
| `eval-cmp-001` | physics | compact | PASS | 3369 ms | 5 | 0 |
| `eval-hin-001` | physics | hinglish | PASS | 4455 ms | 6 | 0 |
| `eval-math-001` | mathematics | conceptual | PASS | 5643 ms | 11 | 1 |
| `eval-math-006` | mathematics | derivation | FAIL | 5167 ms | 0 | 1 |
| `eval-phy-001` | physics | conceptual | FAIL | 4161 ms | 0 | 1 |
| `eval-phy-006` | physics | derivation | PASS | 5464 ms | 12 | 0 |
| `eval-phy-011` | physics | diagram | PASS | 9284 ms | 11 | 3 |
| `eval-phy-014` | physics | comparison | PASS | 3274 ms | 5 | 2 |