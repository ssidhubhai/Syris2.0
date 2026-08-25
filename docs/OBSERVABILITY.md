# OBSERVABILITY.md — Runtime Telemetry

## Every AI request should capture

- request_id;
- session_id;
- provider;
- model;
- task type;
- modality;
- latency;
- token usage if provider exposes it;
- retry count;
- fallback used;
- validation result;
- error class.

## Metrics

### Reliability
- success rate;
- 429 rate;
- 5xx rate;
- schema failure rate;
- validation failure rate;
- fallback rate.

### Performance
- p50/p95 latency;
- time to first useful response;
- render time;
- whiteboard render failures.

### Quality
- benchmark score;
- user correction rate;
- user regeneration rate;
- answer-reference click frequency;
- helpfulness feedback later if implemented.

## Privacy

Use minimal telemetry. Do not log raw student content by default in production without an explicit data policy.
