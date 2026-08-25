# EXPLANATION_SCHEMA.md — Semantic Explanation Contract

## 1. Goal

The LLM must not return a plain wall of text as the primary application contract.
The normalized output is an ExplanationDocument.

## 2. Conceptual shape

```json
{
  "document_id": "...",
  "title": "...",
  "intent": "problem_solution",
  "subject": "physics",
  "language": "hinglish",
  "nodes": [],
  "relationships": [],
  "layout_hints": {},
  "references": [],
  "validation": {},
  "source_metadata": {}
}
```

## 3. Node types

- text
- heading
- equation
- derivation_step
- diagram
- graph
- table
- comparison
- annotation
- callout
- definition
- assumption
- conclusion
- example
- question/checkpoint
- interactive_visual

## 4. Relationship types

- derives_from
- uses
- substitutes_into
- explains
- causes
- contrasts_with
- depends_on
- follows_from
- defines
- references
- highlights
- transforms_into

## 5. Basic Example

```json
{
  "nodes": [
    {"id":"d1","type":"diagram","purpose":"show initial state"},
    {"id":"e1","type":"equation","latex":"\\sum F = ma"},
    {"id":"e2","type":"equation","latex":"F-mg\\sin\\theta = ma"}
  ],
  "relationships": [
    {"from":"d1","to":"e1","type":"explains"},
    {"from":"e1","to":"e2","type":"derives_from"}
  ]
}
```

## 6. Presentation flexibility

The document must not require all node types.
A trivial answer may contain one text node.
A difficult problem may contain a diagram, several equations and many relationships.

## 7. Reference behavior

Every important reusable item should have an ID.
The UI must provide direct jump/highlight behavior for references such as “Equation 2” without forcing manual scrolling.

## 8. Validation metadata

Store:
- math_verified;
- domain_verified;
- verifier_used;
- confidence/uncertainty if the system exposes it;
- unresolved claims.

## 9. Phase 1 Canonical Mock Fixture (Physics — Accelerated Incline)

The following fixture serves as the source-of-truth mock document for Phase 1 Digital Paper testing:

```json
{
  "document_id": "doc-p1-mechanics-incline-001",
  "session_id": "sess-test-001",
  "title": "Maximum Horizontal Acceleration of a Wedge with Friction",
  "intent": "problem_solution",
  "subject": "physics",
  "language": "hinglish",
  "nodes": [
    {
      "id": "node-head-1",
      "type": "heading",
      "content": {
        "text": "Finding Maximum Wedge Acceleration ($a_{\\max}$) Before Upward Slip",
        "level": 1
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-intro-1",
      "type": "text",
      "content": {
        "markdown": "Wedge ke accelerating frame (non-inertial frame) me block par ek pseudo-force $m a_0$ leftward act karega. Jab wedge rightwards acceleration $a_{\\max}$ se move karega, toh block ki tendency incline ke along **upward slip** karne ki hogi. Isliye static friction $f_s$ incline ke along **downward** act karega."
      },
      "importance": "supporting",
      "layout_preference": "full_width"
    },
    {
      "id": "node-sticky-law",
      "type": "definition",
      "content": {
        "title": "Governing Law: Limiting Static Friction",
        "latex": "f_s \\le f_{\\max} = \\mu_s N",
        "annotation": "Critical condition for impending upward slide: $f_s = \\mu_s N$"
      },
      "importance": "critical",
      "layout_preference": "sticky_context"
    },
    {
      "id": "node-diag-fbd",
      "type": "diagram",
      "content": {
        "canvas_type": "PHYSICS_2D",
        "title": "Free Body Diagram in Non-Inertial Frame of Wedge",
        "purpose": "Resolve real gravity, pseudo-force, normal force, and friction into components parallel and perpendicular to the incline.",
        "elements": [
          {
            "id": "elem-incline",
            "type": "polygon",
            "points": [[-5, -3], [5, -3], [5, 3]],
            "label": "Wedge (Angle \\theta)"
          },
          {
            "id": "elem-block",
            "type": "rigid_body",
            "position": {"x": 0.5, "y": 0.3},
            "mass": 2.0,
            "label": "Block (m)"
          },
          {
            "id": "vec-mg",
            "type": "vector",
            "origin": "elem-block.center",
            "direction_deg": 270,
            "magnitude": "m*g",
            "label": "m g (Gravity)",
            "semantic_role": "real_force"
          },
          {
            "id": "vec-pseudo",
            "type": "vector",
            "origin": "elem-block.center",
            "direction_deg": 180,
            "magnitude": "m*a_0",
            "label": "m a_0 (Pseudo Force)",
            "semantic_role": "pseudo_force"
          },
          {
            "id": "vec-normal",
            "type": "vector",
            "origin": "elem-block.center",
            "direction_deg": 120,
            "magnitude": "N",
            "label": "N (Normal Force)",
            "semantic_role": "contact_force"
          },
          {
            "id": "vec-friction",
            "type": "vector",
            "origin": "elem-block.surface_bottom",
            "direction_deg": 210,
            "magnitude": "f_s",
            "label": "f_s (Static Friction)",
            "semantic_role": "friction_force"
          }
        ]
      },
      "importance": "critical",
      "layout_preference": "split_right"
    },
    {
      "id": "node-eq-normal",
      "type": "equation",
      "content": {
        "id_tag": "Eq. (1)",
        "label": "Perpendicular Equilibrium",
        "latex": "N = m g \\cos\\theta + m a_0 \\sin\\theta"
      },
      "importance": "critical",
      "layout_preference": "split_left"
    },
    {
      "id": "node-eq-tangential",
      "type": "equation",
      "content": {
        "id_tag": "Eq. (2)",
        "label": "Parallel Impending Slip Equilibrium",
        "latex": "m a_0 \\cos\\theta = m g \\sin\\theta + f_s"
      },
      "importance": "critical",
      "layout_preference": "split_left"
    },
    {
      "id": "node-deriv-substitute",
      "type": "derivation_step",
      "content": {
        "step_number": 1,
        "title": "Substitute Normal Force into Limiting Friction",
        "explanation": "Impending slip condition $f_s = \\mu_s N$ ko [Eq. (2)](ref://node-eq-tangential) me substitute karte hain, using $N$ from [Eq. (1)](ref://node-eq-normal):",
        "latex": "m a_0 \\cos\\theta = m g \\sin\\theta + \\mu_s (m g \\cos\\theta + m a_0 \\sin\\theta)"
      },
      "importance": "critical",
      "layout_preference": "split_left"
    },
    {
      "id": "node-deriv-isolate",
      "type": "derivation_step",
      "content": {
        "step_number": 2,
        "title": "Isolate Acceleration $a_0$",
        "explanation": "Dono sides se mass $m$ cancel karke $a_0$ terms ko left side me collect karte hain:",
        "latex": "a_0 (\\cos\\theta - \\mu_s \\sin\\theta) = g (\\sin\\theta + \\mu_s \\cos\\theta)"
      },
      "importance": "critical",
      "layout_preference": "split_left"
    },
    {
      "id": "node-conclusion-final",
      "type": "conclusion",
      "content": {
        "title": "Final Maximum Acceleration ($a_{\\max}$)",
        "latex": "a_{\\max} = g \\left( \\frac{\\sin\\theta + \\mu_s \\cos\\theta}{\\cos\\theta - \\mu_s \\sin\\theta} \\right) = g \\left( \\frac{\\tan\\theta + \\mu_s}{1 - \\mu_s \\tan\\theta} \\right)",
        "highlight": true
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-callout-trap",
      "type": "callout",
      "content": {
        "callout_type": "warning",
        "title": "Kota Trap Alert: Boundary Condition Check",
        "markdown": "Agar $\\tan\\theta \\ge \\frac{1}{\\mu_s}$ ho jaye, toh denominator $\\le 0$ ho jayega. Iska physical significance hai ki wedge ko chahe infinite acceleration bhi de do, normal reaction itna increase ho jayega ki friction block ko slip hone hi nahi dega!"
      },
      "importance": "supporting",
      "layout_preference": "full_width"
    }
  ],
  "relationships": [
    {
      "from": "node-diag-fbd",
      "to": "node-eq-normal",
      "type": "explains",
      "label": "Perpendicular force balance"
    },
    {
      "from": "node-diag-fbd",
      "to": "node-eq-tangential",
      "type": "explains",
      "label": "Parallel force balance"
    },
    {
      "from": "node-sticky-law",
      "to": "node-deriv-substitute",
      "type": "uses",
      "label": "Limiting friction condition"
    },
    {
      "from": "node-eq-normal",
      "to": "node-deriv-substitute",
      "type": "substitutes_into",
      "label": "Substitute N"
    },
    {
      "from": "node-eq-tangential",
      "to": "node-deriv-substitute",
      "type": "substitutes_into",
      "label": "Substitute into equilibrium"
    },
    {
      "from": "node-deriv-substitute",
      "to": "node-deriv-isolate",
      "type": "derives_from",
      "label": "Algebraic simplification"
    },
    {
      "from": "node-deriv-isolate",
      "to": "node-conclusion-final",
      "type": "derives_from",
      "label": "Final expression"
    },
    {
      "from": "node-conclusion-final",
      "to": "node-callout-trap",
      "type": "highlights",
      "label": "Denominator singularity check"
    }
  ],
  "layout_hints": {
    "recommended_layout": "hybrid_dual_channel",
    "primary_channel_nodes": ["node-eq-normal", "node-eq-tangential", "node-deriv-substitute", "node-deriv-isolate"],
    "context_channel_nodes": ["node-diag-fbd"],
    "sticky_header_nodes": ["node-sticky-law"]
  },
  "validation": {
    "math_verified": false,
    "domain_verified": false,
    "verifier_used": "not_run_static_fixture",
    "flagged_issues": []
  },
  "source_metadata": {
    "provider": "static_mock_phase1",
    "model": "handcrafted_canonical_physics_v1",
    "generation_time_ms": 0
  }
}
```
