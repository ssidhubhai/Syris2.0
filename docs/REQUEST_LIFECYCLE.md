# REQUEST_LIFECYCLE.md — Request and Error Pipeline

## 1. Standard request

```text
Client
 ↓
request_id/idempotency key
 ↓
Gateway validation
 ↓
Load session
 ↓
Analyze input/context
 ↓
Need AI?
 ├─ no → local/database action
 └─ yes
      ↓
Presentation requirements
      ↓
AI Control Plane
      ↓
Provider/model
      ↓
Stream/receive result
      ↓
Parse
      ↓
Schema validation
      ↓
Semantic/domain validation
      ↓
Normalize to ExplanationDocument
      ↓
Persist
      ↓
Render/stream to client
```

## 2. No-AI path examples

- open history;
- replay whiteboard;
- zoom/pan;
- expand/collapse;
- jump-to-reference;
- deterministic algebra check;
- save state.

## 3. Transient errors

Examples:
- HTTP 429;
- HTTP 5xx;
- network timeout.

Strategy:
- bounded retry with jitter;
- then fallback provider/model;
- keep the session state safe;
- surface a graceful UI state.

## 4. Permanent errors

Examples:
- invalid request;
- unsupported model;
- invalid API version;
- auth failure.

Do not blindly retry.

## 5. AI output failure

```text
invalid JSON/schema
 ↓
retry or fallback once
 ↓
if still invalid → safe error / regenerate constrained response
```

Never render invalid state.

## 6. Duplicate request

Use request IDs and idempotency.
Repeated submission should return the existing operation/result where possible.

## 7. Network disconnect during streaming

Persist the latest committed explanation state.
On reconnect, resume from the last durable state rather than restarting the whole interaction blindly.

## 8. Session persistence rule

Persist:
- original user input;
- model request metadata;
- normalized explanation document;
- whiteboard state;
- conversation state;
- validation result;
- provider/model used.
