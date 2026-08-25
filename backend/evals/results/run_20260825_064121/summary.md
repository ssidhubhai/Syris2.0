# Evaluation Run Summary: `eval_run_20260825_064121`

- **Timestamp**: 2026-08-25T06:42:12.120776+00:00
- **Mode**: `live_gemini`
- **Model**: `gemini-3.5-flash-lite`
- **Prompt Version**: `v1.0`
- **Total Cases**: 10 (Success: 10, Fail: 0)

---

## Latency Breakdown Summary

| Metric | Duration (ms) | % of Total |
|---|---|---|
| **Deterministic Preprocessing** | 0.37 ms | 0.0% |
| **Gemini Structured Call** | 5071.19 ms | 100.0% |
| **Average Total Pipeline** | 5073.02 ms | 100.0% |

---

## Failure Distribution (Taxonomy A–J)

| Category Code | Failure Count |
|---|---|
| `B_INCORRECT_REASONING` | 6 |
| `E_MISSING_USEFUL_VISUAL` | 1 |

---

## Case-by-Case Breakdown

| Case ID | Subject | Category | Status | Latency | Nodes | Failures |
|---|---|---|---|---|---|---|
| `eval-chem-001` | chemistry | conceptual | PASS | 4815 ms | 6 | 0 |
| `eval-chem-008` | chemistry | mechanism | PASS | 4313 ms | 5 | 0 |
| `eval-cmp-001` | physics | compact | PASS | 3501 ms | 6 | 0 |
| `eval-hin-001` | physics | hinglish | PASS | 4485 ms | 6 | 2 |
| `eval-math-001` | mathematics | conceptual | PASS | 12094 ms | 9 | 1 |
| `eval-math-006` | mathematics | derivation | PASS | 5374 ms | 10 | 0 |
| `eval-phy-001` | physics | conceptual | PASS | 4297 ms | 8 | 0 |
| `eval-phy-006` | physics | derivation | PASS | 4058 ms | 7 | 0 |
| `eval-phy-011` | physics | diagram | PASS | 3825 ms | 7 | 2 |
| `eval-phy-014` | physics | comparison | PASS | 3964 ms | 6 | 2 |