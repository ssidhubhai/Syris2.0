# DECISIONS.md — V1 Architectural Decisions & Invariants

## Confirmed Architectural Decisions

### D001 — Adaptive Digital Study Sheet / Digital Paper
- **Decision**: V1 is an adaptive Digital Study Sheet / Digital Paper experience; it is not a chat-first transcript.
- **Rationale**: Eliminates the presentation and cognitive gap where students lose context and must constantly scroll to connect ideas, formulas, and diagrams.

### D002 — Not a Simulated Classroom or Full LMS
- **Decision**: V1 is not an AI classroom simulator, not a full coaching replacement, and not an LMS/gamification platform.
- **Rationale**: Keeps the scope tightly focused on solving the explanation presentation and understanding problem.

### D003 — Dynamic Adaptive Representation (No Universal Template)
- **Decision**: V1 does not use a universal explanation template (e.g., text + diagram + flowchart + equation + animation for every request). Explanations are dynamically composed based on user intent, subject, question type, and complexity.
- **Rationale**: Different problems require different representations; enforcing a universal template creates unnecessary cognitive overhead.

### D004 — Contextual Visual Generation (No Universal Visual Maximum)
- **Decision**: Visual elements (diagrams, graphs, coordinate planes) are generated only when contextually useful and explanatory. There is no universal diagram/visual maximum; multiple diagrams are permitted when representing meaningful state changes (e.g., $t=0 \to t=dt$, multi-stage chemical reactions, complementary projections). Unnecessary or purely decorative visuals are strictly rejected.
- **Rationale**: Visuals must serve a pedagogical purpose and reduce cognitive load, not decorate the page.

### D005 — Semantic AI Output + Deterministic Application Layout
- **Decision**: The AI layer produces semantic explanation content nodes and relationship edges (`ExplanationDocument`). Deterministic application code strictly controls coordinate calculation, layout positioning, responsive reflow, and rendering. The LLM is never asked to generate arbitrary pixel coordinates or CSS layouts.
- **Rationale**: Enforces reliability, responsive cross-device consistency, and clean separation of concerns.

### D006 — Provider Abstraction & Canonical Schema Boundary
- **Decision**: The frontend must never depend on provider-specific model output formats. All AI providers are abstracted behind the AI Control Plane and normalized into the canonical `ExplanationDocument` schema.
- **Rationale**: Enables multi-provider routing, transparent fallback, and shielding client applications from third-party API changes.

### D007 — Model Verification & Fail-Closed Policy
- **Decision**: Model availability, capabilities, and API endpoints must be verified against live provider metadata and current official documentation. Unknown, deprecated, unverified, or uncertified models must fail closed and cannot enter the active routing pool.
- **Rationale**: Prevents hallucinations of obsolete model IDs and runtime execution failures.

### D008 — Phase 1 Isolation (No Live AI, No Streaming)
- **Decision**: Phase 1 contains no live AI calls and no streaming protocols (TTFP/SSE). Phase 1 strictly proves the static Digital Paper and `ExplanationDocument` rendering system using mock documents.
- **Rationale**: Ensures the visual and mathematical layout foundation is fully robust and testable before introducing network and streaming complexity.

### D009 — Persistence Architecture (PostgreSQL Primary; Neo4j/Qdrant Deferred)
- **Decision**: PostgreSQL (relational tables + JSONB documents) serves as the V1 persistence layer for sessions, messages, problems, attempts, explanation documents, whiteboard states, and model telemetry. Heavy external graph databases (Neo4j) and vector databases (Qdrant) are deferred to post-V1.
- **Rationale**: Minimizes operational complexity while retaining structured relational integrity and rich document querying.

### D010 — Math Rendering Foundation (KaTeX Read-Only)
- **Decision**: KaTeX is the initial read-only mathematical typesetting renderer for all formula nodes in V1. (MathLive evaluation is deferred until interactive student formula input is implemented).
- **Rationale**: High-performance, battle-tested, lightweight LaTeX typesetting for browser rendering.

### D011 — Visual Whiteboard Rendering (2D SVG / Canvas)
- **Decision**: Declarative 2D Parametric SVG and HTML5 Canvas are the visual rendering strategy for Free Body Diagrams, coordinate graphs, and chemical structures. 3D WebGL / Three.js geometry is deferred to post-V1.
- **Rationale**: Provides deterministic, high-performance, responsive vector rendering without heavy 3D engine overhead.

### D012 — Scope Boundaries (Voice, 3D, and Collaboration Post-V1)
- **Decision**: Full-duplex voice interaction (Gemini Live), 3D coordinate viewports, and multi-user collaborative study rooms (Yjs CRDTs) are confirmed as post-V1 capabilities.
- **Rationale**: Protects V1 execution velocity and focuses all resources on the core Digital Study Sheet value proposition.

### D013 — Phase 1 Deterministic Hybrid Document-DAG Layout Engine
- **Decision**: Phase 1 implements a lightweight deterministic Hybrid Document-DAG Layout Engine in pure TypeScript/CSS. Primary reading and derivations flow vertically through a main content channel, contextual visuals and callouts are partitioned into an adjacent context channel (reflowing inline on compact viewports), and relationship connector splines are rendered via an absolute SVG Bézier curve overlay. Heavy third-party graph layout libraries (Dagre, Cytoscape, Elkjs) are rejected for the core study sheet.
- **Rationale**: Delivers 100% deterministic layout, zero bundle bloat, native browser text selection, excellent mobile responsiveness, and high solo-developer maintainability.

### D014 — Phase 1 Canonical Physics Mock Fixture Definition
- **Decision**: Phase 1 testing and validation uses a standardized JEE Advanced physics fixture (*"Maximum Horizontal Acceleration of a Wedge with Friction"*). The fixture validates all 15 node types, 12 relationship types, 2D vector FBD graphics, sticky context laws, callouts, and jump-to-reference anchors in a realistic, non-decorative problem setting.
- **Rationale**: Provides a concrete, mathematically rigorous benchmark for testing Digital Paper rendering without requiring network AI calls.

---

## Implementation-Time Verification Requirements

Before implementing any subsystem, the engineering agent must not rely on memory or historical notes and MUST explicitly verify the following against current official documentation and live provider metadata:

1. **Gemini SDK**: Verify the active official SDK (`google-genai` for Python / `@google/genai` for TypeScript), supported installation packages, and exact client invocation patterns.
2. **Gemini API Version**: Verify the active stable API surface (e.g., `v1`) and supported protocol endpoints.
3. **Gemini Model IDs & Lifecycle**: Query live provider metadata (e.g., `client.models.list()`) to obtain currently active, supported model IDs; never adopt hardcoded model strings from legacy documentation.
4. **Secondary Providers (Mistral / NVIDIA / OpenRouter)**: Verify live endpoint availability, Free mode allowances, quotas, and structured output support prior to implementing adapters.
5. **Rate Limits & Quotas**: Dynamically inspect and respect provider rate limits, concurrency limits, and retry headers.
6. **Streaming & Chunking Behavior**: Verify chunking consistency and token framing in live integration tests.
7. **Package & Framework Versions**: Verify active compatibility across Next.js, React, FastAPI, Pydantic (v2), SQLAlchemy (v2), and SymPy before locking dependency manifests.
