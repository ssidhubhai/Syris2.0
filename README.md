# AI JEE Study Companion — Blueprint Pack

This folder is the source-of-truth starter pack for the V1 build.

## Core thesis

The product is not a coaching platform and not a classroom simulator.
It is an AI study companion that takes the answer/reasoning produced by modern AI and turns it into a highly usable, visually connected digital study sheet.

The product must solve the presentation gap of normal chat-based AI:
- references should remain reachable;
- related equations/steps should stay visually connected;
- diagrams should appear only when they improve understanding;
- multiple diagrams should appear only when the context requires them;
- the layout should adapt to the answer rather than forcing one template;
- the student should be able to understand the flow without repeatedly scrolling back through a long response.

## Source-of-truth hierarchy

1. Provider runtime/API metadata for availability.
2. Official provider documentation for supported API behavior.
3. This repository's approved registry and architecture contracts.
4. Automated evaluations and production telemetry.
5. Agent memory or old tutorials: NEVER authoritative.

## Important legacy note

`docs/original-architecture-blueprint.pdf` is the historical architecture reference supplied for this project. It contains valuable concepts such as dynamic blackboard rendering, Socratic escalation, prerequisite graphs, error vaults, and typed streaming, but some provider/model details are time-sensitive and must not be copied blindly.

## Recommended reading order for an engineering agent

1. AGENTS.md
2. docs/PRODUCT.md
3. docs/ARCHITECTURE.md
4. docs/AI_GATEWAY.md
5. docs/EXPLANATION_SCHEMA.md
6. docs/WHITEBOARD_DSL.md
7. docs/UI_BLUEPRINT.md
8. docs/REQUEST_LIFECYCLE.md
9. docs/VALIDATION.md
10. docs/EVALUATION.md
11. docs/DATA_MODEL.md
12. docs/SECURITY.md
13. docs/OBSERVABILITY.md
14. docs/DEVELOPMENT_PLAN.md
15. config/PROVIDER_REGISTRY.example.yaml
