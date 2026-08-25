# UI_BLUEPRINT.md — Adaptive Digital Paper UI

## 1. Design goal

The UI exists to remove the presentation gap of chat AI.

The user should feel that the solution has a coherent spatial structure, even when the underlying answer is generated dynamically.

## 2. Main shell

Minimal navigation:
- Home
- History
- Practice
- Concepts
- Mistakes

The Study Workspace is the main product.

## 3. Study Workspace

```text
┌──────────────────────────────────────────────────────┐
│ minimal header                                       │
├──────────────────────────────────────────────────────┤
│                                                      │
│                  DIGITAL PAPER                       │
│                                                      │
│     question / explanation / diagrams / math         │
│                                                      │
│                                                      │
├──────────────────────────────────────────────────────┤
│ ask / follow-up / upload / voice                     │
└──────────────────────────────────────────────────────┘
```

The canvas should use the available screen area aggressively while preserving comfortable reading width.

## 4. Digital paper behavior

Paper is a semantic canvas, not a literal A4 sheet requirement.
It may expand vertically and use side-by-side regions when relationships benefit from them.

## 5. Adaptive layout: Deterministic Hybrid Document-DAG Engine

The frontend uses a lightweight, deterministic **Hybrid Document-DAG Layout Engine** (pure TypeScript/CSS) instead of an external graph layout library:

### 5.1 Dual-Channel Responsive Architecture
- **Desktop (Viewport Width $\ge 1024\text{px}$)**:
  - **Primary Derivation Channel**: Vertical flow containing problem statements, step-by-step mathematical transformations, and derivations.
  - **Context Visual Channel**: Parallel adjacent region anchoring contextual 2D diagrams, sticky governing laws, and teacher trap callouts alongside the derivation steps that depend on them.
- **Tablet / Mobile (Viewport Width $< 1024\text{px}$)**:
  - Automatically reflows into a single linear stacked stream while preserving full-width diagram visibility, inline expanders, and sticky header pinning.

### 5.2 Deterministic SVG Bézier Connector Routing
- Evaluates DOM bounding rects for source and target node cards.
- Computes non-intersecting cubic Bézier spline paths:
  $$\mathbf{B}(t) = (1-t)^3 \mathbf{P}_0 + 3(1-t)^2 t \mathbf{P}_1 + 3(1-t) t^2 \mathbf{P}_2 + t^3 \mathbf{P}_3$$
- Renders smooth glowing connection curves in an absolute SVG overlay when a relationship is hovered or focused via jump-to-reference.

### 5.3 Layout Input Parameters
Layout decisions depend dynamically on:
- Content node sequence and importance (`critical`, `supporting`, `note`);
- Explicit semantic relationship edges (`derives_from`, `explains`, `substitutes_into`, `uses`);
- Diagram aspect ratio and dimensions;
- Active viewport width and container constraints;
- Natural reading order without algorithmic graph inversion.

## 6. Colour philosophy

Avoid neon-heavy themes and visual noise.
Use a mostly neutral foundation plus a small semantic accent system.

Suggested roles:
- canvas/background;
- primary ink;
- muted text;
- primary action;
- subject accent;
- relation connector;
- success;
- warning;
- error;
- selection/focus.

The exact hex values must be chosen after visual testing. Do not hard-code many colors across components.

## 7. Subject accents

Use subtle subject identity, not separate app themes.
Example direction:
- Physics: blue/cyan family;
- Mathematics: indigo/violet family;
- Chemistry: amber/coral family.

These are starting directions, not final locked colors.

## 8. Typography

Use a highly readable UI font for prose.
Use KaTeX/MathLive for mathematical notation.
Use handwritten-like styling only for occasional teacher-note annotations, not for whole paragraphs.

## 9. Visual rhythm

Avoid long uninterrupted paragraphs.
Prefer:
- concise explanation;
- relevant visual anchor;
- equation/transformation;
- annotation;
- next logical step.

But do not force this sequence.

## 10. Navigation through reasoning

Every referenced step/equation/diagram should be jumpable.
Clicking a reference should highlight the source and return focus to the current step.

## 11. Context retention

Provide an optional sticky context region for relevant equations/definitions/diagram states when scrolling would otherwise create cognitive friction.
Context must be selected dynamically.

## 12. Focus mode

Allow the user to focus a step while keeping a small amount of surrounding context visible.

## 13. Motion

Use animation only when it explains a transformation, relationship or state change.
Avoid decorative animation on every component.

## 14. Accessibility

Respect readable font sizes, contrast, keyboard navigation, reduced motion, and semantic labels for visual elements.
Math and diagrams should have text equivalents where practical.
