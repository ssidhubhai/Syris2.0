# AGENTS.md — AI JEE Study Companion Engineering Rules

## 0. Role

You are an implementation agent working under a human product owner/architect.
Do not invent product scope. Do not silently redesign architecture. Do not substitute assumptions for verification.

## 1. Product identity

This project is an AI study companion for JEE aspirants.

V1 is centered on one problem:

> Modern AI can often produce a correct answer, but the answer is dumped into a scrolling chat transcript. This project transforms the response into a visually connected, adaptive digital study sheet so the student can see how ideas, equations, diagrams, annotations and derivations relate.

The product is NOT V1 coaching, NOT a full classroom simulator, and NOT an LMS.

## 2. Non-negotiable presentation principle

Never use a universal answer template such as:

text + diagram + flowchart + equation + animation

for every request.

The system must dynamically decide presentation based on:
- user intent;
- subject;
- question type;
- difficulty/complexity;
- current conversation context;
- student-provided work/image;
- dependency/relationship structure;
- whether a visual representation reduces cognitive load;
- available screen space;
- device constraints.

Possible representations include:
- text;
- equation;
- derivation;
- diagram;
- multiple diagrams;
- flow;
- comparison;
- graph;
- table;
- annotation;
- timeline;
- interactive visualization;
- mixed composition.

A representation must have an explanatory purpose. No decorative visual generation.

## 3. Semantic vs rendering boundary

The AI/model layer determines:
- what is correct;
- what needs to be explained;
- what relationships exist;
- what representation type is useful;
- what diagram/equation semantics are required.

The deterministic application layer determines:
- exact layout;
- coordinates;
- spacing;
- typography;
- responsive behavior;
- rendering;
- interaction behavior.

Do not ask the LLM to generate arbitrary pixel coordinates or CSS layout for the whole page.

## 4. AI provider truth

Never trust an LLM's memory for:
- model IDs;
- API versions;
- model lifecycle;
- provider capabilities;
- pricing;
- quotas/rate limits;
- SDK methods;
- deprecation dates.

Before implementing provider/model/API behavior, verify against current official provider documentation and live provider metadata where the provider exposes it.

For Gemini, use the current official API surface. Do not resurrect historical Gemini 1.x/2.x models or obsolete examples. Model availability must be verified at runtime/registry level.

## 5. Provider abstraction

Frontend and Teacher Engine must never depend on provider-specific response shapes.
All providers must normalize into internal contracts.

## 6. Model certification

A model may enter the routing pool only if:
1. it is in the approved registry;
2. provider discovery/metadata confirms availability where possible;
3. required capabilities are verified;
4. integration tests pass;
5. evaluation benchmark passes the configured threshold;
6. it has a documented fallback strategy.

Unknown/deprecated/uncertified models must fail closed.

## 7. Reliability

Implement:
- request IDs;
- idempotency/deduplication;
- timeout handling;
- exponential backoff with jitter for transient errors;
- provider fallbacks;
- circuit breakers;
- schema validation;
- semantic validation where required;
- persistent session state;
- graceful degradation.

Never retry permanent errors indefinitely.

## 8. AI output safety

Never render an AI response directly.
Pipeline:
model output → parse → schema validation → semantic/domain validation where applicable → normalize → render.

Malformed or uncertified output must not be rendered.

## 9. Scope control

Do not add unsolicited:
- gamification;
- social feeds;
- leaderboards;
- course/LMS infrastructure;
- classroom simulation;
- giant analytics dashboards;
- collaborative rooms;
- arbitrary microservices.

Implement the smallest modular system that satisfies the contracts.

## 10. Change discipline

Before changing an architectural contract:
1. read all relevant docs;
2. inspect existing implementation;
3. identify consumers;
4. propose the change;
5. update the contract/docs;
6. update tests;
7. then implement.

Do not silently break schemas.

## 11. Security

Never expose provider API keys in browser/client code.
Never commit secrets.
Use environment/secret configuration.
Validate uploaded files and input sizes.

## 12. Definition of done

For any implementation task:
- code implemented;
- tests added/updated;
- type checking passes;
- lint passes;
- existing relevant tests pass;
- error handling included;
- no secrets added;
- browser verification performed for UI changes;
- docs updated when contracts change;
- final summary states changed files, tests run, and known limitations.

## 13. Before coding a new subsystem

Read the relevant contract first. If a necessary contract does not exist, stop and create/update the contract instead of inventing implementation behavior inline.
