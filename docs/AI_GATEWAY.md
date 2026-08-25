# AI_GATEWAY.md — Multi-Provider AI Control Plane

<!-- VERIFIED_ON: 2026-08-25 -->

## 1. Purpose

The AI Control Plane makes provider/model selection reliable and replaceable.

It prevents obsolete-model hallucinations, handles provider failure, and routes different tasks to appropriate models.

## 2. Source-of-truth hierarchy

Runtime provider metadata (`client.models.list()`) > official docs > approved registry > benchmark results > agent memory.

## 3. Provider interface

Each provider adapter should conceptually support:

```python
class ModelProvider:
    async def list_models(): ...
    async def get_model(model_id): ...
    async def generate(request): ...
    async def stream(request): ...
    async def health_check(): ...
```

Usage/quotas may be provider-specific; represent them through normalized telemetry rather than assuming identical APIs.

## 4. Model registry

Each model record includes:
- provider;
- exact model ID;
- API version;
- lifecycle/status;
- allowed environments;
- modalities;
- context limit if known;
- output limit if known;
- structured output support;
- tool/function support;
- streaming support;
- capabilities;
- benchmark scores;
- current certification state;
- last verified timestamp (`last_verified_at`).

## 5. Model eligibility

A model is eligible only if:
- approved in the verified registry;
- currently available from live discovery;
- capability-compatible (e.g. structured output + multimodal);
- healthy enough (circuit breaker closed);
- within local safety/policy limits.

## 6. Routing input

Router receives:
- task type;
- modality;
- subject;
- complexity;
- language;
- required output types;
- latency target;
- quota/health signals.

## 7. Routing output

```json
{
  "provider": "google",
  "model": "gemini-3.5-flash-lite",
  "reason": "multimodal teacher task",
  "fallback_chain": ["google/gemini-3.5-flash", "google/gemini-2.5-flash"]
}
```

## 8. Routing principle

Prefer one model for normal requests.
Use a verifier only when complexity/risk/confidence justifies it.
Do not call multiple models for every request.

## 9. Fallback & Error Classification

| Error | Category | Behavior |
| :--- | :--- | :--- |
| `503 Service Unavailable` | Transient | Exponential backoff with jitter, then fallback model |
| `429 Resource Exhausted` | Transient/Quota | Backoff if rate limit; route to secondary provider if quota exhausted |
| `400 Bad Request` | Permanent | Fail closed; do NOT retry |
| `401 / 403 Auth Failure` | Permanent | Fail closed; disable provider |
| `404 Model Not Found` | Permanent | Remove model from active routing pool |

## 10. Circuit breaker

Track provider/model failure rates.
Open the circuit temporarily after repeated transient failures.
Probe after cooldown.

## 11. Deduplication

Every client request receives a request ID/idempotency key.
Duplicate operations must return/reuse the existing result when safe.

## 12. Cost/quota rule

Do not use a large model for tasks that can be handled locally or by a smaller model.
Examples:
- simple metadata classification;
- local render operations;
- deterministic math checks;
- session replay.

## 13. Gemini-specific rule (Verified on 2026-08-25)

Never hard-code historical Gemini model IDs from memory.
- Current Official SDK: `google-genai` (v2.19.0+)
- Official Client: `from google import genai; client = genai.Client()`
- Live discovery mechanism: `client.models.list()`
- Verified active candidates: `gemini-3.5-flash-lite`, `gemini-3.5-flash`, `gemini-2.5-flash`, `gemini-3.7-flash`
- Discontinued / Rejected: `gemini-2.5-pro` (deprecated by Google for new users), `gemini-2.0-flash`, `gemini-1.5-pro`, `gemini-1.5-flash`

## 14. Provider independence

Teacher Engine must know task/capability abstractions, not provider-specific SDK details.
Only provider adapters know provider API syntax.
