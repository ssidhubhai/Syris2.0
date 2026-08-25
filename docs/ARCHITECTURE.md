# ARCHITECTURE.md — V1 System Architecture

## 1. Top-level architecture

```text
Student
  ↓
Study Workspace
  ↓
API Gateway
  ↓
Session Manager
  ↓
Context Analyzer
  ↓
Presentation Planner
  ↓
AI Control Plane
  ↓
Provider Adapter(s)
  ↓
Response Normalizer
  ↓
Semantic/Domain Validation
  ↓
ExplanationDocument
  ↓
Layout Engine
  ↓
Digital Paper Renderer
  ↓
Student
```

## 2. Major modules

### Frontend
Responsibilities:
- digital paper rendering;
- user input;
- local interaction state;
- canvas/diagram interaction;
- equation rendering;
- responsive behavior;
- session replay.

### Backend/API Gateway
Responsibilities:
- authentication;
- request validation;
- request IDs/idempotency;
- session loading;
- orchestration;
- provider communication;
- persistence;
- error normalization.

### Context Analyzer
Extracts:
- intent;
- subject;
- chapter/concept if confidently identifiable;
- question complexity;
- user-provided attempt;
- desired help level;
- relevant prior context.

### Presentation Planner
Chooses representations dynamically.
It does NOT directly generate pixels.

### AI Control Plane
Owns:
- provider registry;
- model discovery/certification;
- capability filtering;
- routing;
- health;
- quota signals;
- retry/fallback;
- circuit breakers;
- model evaluation metadata.

### Explanation Composer
Converts model result + presentation plan into a normalized ExplanationDocument.

### Layout Engine
Turns semantic nodes/relationships into layout regions.
Use deterministic graph/layout algorithms where applicable.

### Renderers
- text renderer;
- math renderer;
- SVG/Canvas renderer;
- optional WebGL renderer later.

### Validation
- schema validation;
- algebraic verification;
- domain rules;
- chemical validation where applicable;
- cross-model verification for high-risk cases.

## 3. V1 simplification

Do not begin with microservices. Use clear internal modules in one backend. Extract services later only if measured load/complexity requires it.

## 4. Recommended stack direction

Frontend: React/Next.js + TypeScript.
Backend: FastAPI/Python or equivalent strongly typed server boundary.
Database: PostgreSQL.
Math: KaTeX/MathLive frontend; SymPy backend verification.
Graphics: SVG/Canvas first; Three.js/WebGL later where justified.

Exact framework versions must be verified when implementation starts.
