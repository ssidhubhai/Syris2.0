# DEVELOPMENT_PLAN.md — Solo Developer Build Order

## Phase 0 — Architecture only

Deliver:
- repository structure;
- contracts;
- schemas;
- provider registry template;
- UI blueprint;
- benchmark harness skeleton.

No production feature coding.

## Phase 1 — Digital Paper prototype

Build a hardcoded explanation document and render:
- heading;
- text;
- equation;
- diagram;
- relationship arrow;
- annotation;
- jump-to-reference.

Goal: prove the presentation concept without AI.

## Phase 2 — Core session backend

Implement:
- session;
- message persistence;
- explanation document persistence;
- history restore;
- request IDs/idempotency.

## Phase 3 — One AI provider

Integrate one currently verified Gemini model/API.
Output must be normalized into ExplanationDocument.

## Phase 4 — Context + Presentation Planner

Implement intent/complexity/context analysis and adaptive representation selection.

## Phase 5 — Multimodal input

Add question image + student attempt image.

## Phase 6 — Validation

Add schema validation and deterministic verification paths.

## Phase 7 — Second provider

Add one alternate provider only after provider abstraction is proven.

## Phase 8 — Reliability

Add retries, fallbacks, circuit breaker, health, quota signals.

## Phase 9 — Evaluation

Build and continuously expand golden JEE test set.

## Phase 10 — UI polish/performance

Tune typography, colors, layout, motion, responsiveness, caching, and rendering performance based on actual student testing.

## Phase 11 — Optional later features

- voice;
- richer 3D;
- deeper mistake memory;
- prerequisite graph;
- practice generation;
- collaboration.

Do not pull these into V1 unless a concrete user need emerges.
