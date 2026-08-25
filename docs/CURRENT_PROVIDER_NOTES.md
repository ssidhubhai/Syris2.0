# CURRENT_PROVIDER_NOTES.md — Time-Sensitive Provider Facts

<!-- VERIFIED_ON: 2026-08-25 -->

This document captures time-sensitive facts verified via live Google GenAI API inspection and official documentation on **2026-08-25**.

---

## 1. Official Google GenAI SDK & API Surface

- **Verified SDK Package**: `google-genai` (`v2.19.0`)
- **Deprecated Legacy SDKs**: `google-generativeai` (Python) and `@google/generative-ai` (JS/TS) must NEVER be used.
- **Client Initialization**: `from google import genai; client = genai.Client(api_key=...)`
- **Stable API Version**: `v1` (endpoints under `genai.Client().models`)
- **Authentication**: `GEMINI_API_KEY` or `GOOGLE_API_KEY` loaded via environment variables.

---

## 2. Live Discovered Model Catalog (Verified: 2026-08-25)

Empirical results from running `backend/scripts/discover_gemini_models.py` against live Google GenAI endpoints:

### Active & Verified Available Models
| Model ID | Display Name | Input Token Limit | Output Token Limit | Verified Capabilities | Status / Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `gemini-3.5-flash-lite` | Gemini 3.5 Flash Lite | 1,048,576 | 65,536 | Text, Structured Output (JSON Schema), Multimodal | **Active & Verified** (Primary high-throughput candidate) |
| `gemini-3.5-flash` | Gemini 3.5 Flash | 1,048,576 | 65,536 | Text, Structured Output (JSON Schema), Multimodal | **Active & Verified** (Balanced quality/latency candidate) |
| `gemini-2.5-flash` | Gemini 2.5 Flash | 1,048,576 | 65,536 | Text, Structured Output (JSON Schema), Multimodal | **Active & Verified** (Stable fallback) |
| `gemini-3.7-flash` | Gemini 3.7 Flash | 1,048,576 | 65,536 | Text, Multimodal, Agentic | Active in catalog; observed transient HTTP 503 during peak load testing |
| `gemini-3.1-pro-preview` | Gemini 3.1 Pro Preview | 1,048,576 | 65,536 | Complex Reasoning, Tool Usage | Active in catalog; requires paid quota / tier (Free tier limit 0) |
| `gemma-4-31b-it` | Gemma 4 31B IT | 262,144 | 32,768 | Open-weights instruction model | Active in catalog |
| `gemma-4-26b-a4b-it` | Gemma 4 26B A4B IT | 262,144 | 32,768 | MoE instruction model | Active in catalog |

### Deprecated / Removed / Inactive Models
| Model ID | Observed Live Status | Action |
| :--- | :--- | :--- |
| `gemini-2.5-pro` | **HTTP 404**: *"This model models/gemini-2.5-pro is no longer available to new users. Please update your code to use models/gemini-3.1-pro-preview..."* | Rejected / Fail Closed |
| `gemini-2.0-flash` | **Not Found**: Not present in live discovery catalog | Rejected / Fail Closed |
| `gemini-1.5-pro` | **Not Found**: Not present in live discovery catalog | Rejected / Fail Closed |
| `gemini-1.5-flash` | **Not Found**: Not present in live discovery catalog | Rejected / Fail Closed |

---

## 3. Observed Error Behaviors & Classification

| Error Code | Provider Classification | System Behavior |
| :--- | :--- | :--- |
| `503 Service Unavailable` | Transient / High demand spike | Retry with exponential backoff & jitter; failover to `gemini-3.5-flash-lite` |
| `429 Resource Exhausted` | Transient / Quota limit reached | Backoff if rate limit; failover to secondary provider/model if daily quota exhausted |
| `400 Bad Request` | Permanent client error (invalid arguments) | Fail closed, normalize into `INVALID_PAYLOAD` |
| `401 / 403 Auth / Permission` | Permanent auth error | Fail closed, alert operator |
| `404 Not Found` | Permanent (model deprecated/unavailable) | Fail closed, exclude model from active routing pool |

---

## 4. Unresolved Questions for Future Phases

1. Rate limits on Free tier for `gemini-3.7-flash` vs `gemini-3.5-flash-lite`.
2. Multimodal latency benchmark for JEE diagram uploads.
3. Secondary provider certification (Mistral / NVIDIA) when Phase 7 begins.
