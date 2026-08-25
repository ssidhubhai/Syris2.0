import { ExplanationDocument } from '@/types/explanation';

/**
 * Frozen Real-AI Regression Fixture for Phase 4C
 * Case: Simple Pendulum Time Period Derivation (derivation)
 * Query: "Derive the time period formula T = 2\pi\sqrt{L/g} of a simple pendulum for small angular displacements using the restoring torque equation."
 * Model: gemini-3.5-flash-lite | Prompt: v1.0
 */
export const case_4_phy_pendulum_fixture: ExplanationDocument = {
  "document_id": "doc-ce697096",
  "session_id": "sess-p4c-890bd5b6",
  "title": "Derivation of Time Period of a Simple Pendulum",
  "intent": "derivation",
  "subject": "physics",
  "language": "english",
  "nodes": [
    {
      "id": "node-head-1",
      "type": "heading",
      "content": {
        "text": "Derivation of Time Period of a Simple Pendulum",
        "level": 1
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-text-1",
      "type": "text",
      "content": {
        "markdown": "A simple pendulum consists of a point mass $m$ (bob) suspended from a rigid support by a light, inextensible string of length $L$. When displaced by a small angle $\\theta$ from its mean position and released, it executes Simple Harmonic Motion (SHM). We will use the restoring torque method to derive its time period."
      },
      "importance": "supporting",
      "layout_preference": "full_width"
    },
    {
      "id": "node-def-1",
      "type": "definition",
      "content": {
        "title": "Restoring Torque for a Simple Pendulum",
        "latex": "\\tau = -mgL \\sin\\theta",
        "annotation": "Negative sign indicates that torque acts in the direction opposite to angular displacement."
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-deriv-1",
      "type": "derivation_step",
      "content": {
        "latex": "\\text{Step 1}",
        "step_number": 1,
        "explanation": "Algebraic derivation step 1"
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-deriv-2",
      "type": "derivation_step",
      "content": {
        "latex": "\\text{Step 2}",
        "step_number": 2,
        "explanation": "Algebraic derivation step 2"
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-deriv-3",
      "type": "derivation_step",
      "content": {
        "latex": "\\text{Step 3}",
        "step_number": 3,
        "explanation": "Algebraic derivation step 3"
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-eq-1",
      "type": "equation",
      "content": {
        "latex": "Angular Simple Harmonic Motion Equation",
        "id_tag": "Eq. (1)",
        "label": "Angular Simple Harmonic Motion Equation"
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-callout-1",
      "type": "callout",
      "content": {
        "markdown": "Important concept regarding trap.",
        "title": "trap",
        "callout_type": "trap"
      },
      "importance": "note",
      "layout_preference": "full_width"
    },
    {
      "id": "node-conc-1",
      "type": "conclusion",
      "content": {
        "title": "Time Period Formula",
        "latex": "T = 2\\pi\\sqrt{\\frac{L}{g}}",
        "highlight": true
      },
      "importance": "critical",
      "layout_preference": "full_width"
    }
  ],
  "relationships": [
    {
      "from": "node-head-1",
      "to": "node-text-1",
      "type": "explains"
    },
    {
      "from": "node-text-1",
      "to": "node-def-1",
      "type": "defines"
    },
    {
      "from": "node-def-1",
      "to": "node-deriv-1",
      "type": "derives_from"
    },
    {
      "from": "node-deriv-1",
      "to": "node-deriv-2",
      "type": "follows_from"
    },
    {
      "from": "node-deriv-2",
      "to": "node-deriv-3",
      "type": "substitutes_into"
    },
    {
      "from": "node-deriv-3",
      "to": "node-eq-1",
      "type": "derives_from"
    },
    {
      "from": "node-eq-1",
      "to": "node-conc-1",
      "type": "derives_from"
    },
    {
      "from": "node-conc-1",
      "to": "node-callout-1",
      "type": "highlights"
    }
  ],
  "layout_hints": {
    "recommended_layout": "linear_flow",
    "primary_channel_nodes": [
      "node-head-1",
      "node-text-1",
      "node-def-1",
      "node-deriv-1",
      "node-deriv-2",
      "node-deriv-3",
      "node-eq-1",
      "node-conc-1"
    ],
    "context_channel_nodes": [
      "node-callout-1"
    ],
    "sticky_header_nodes": [
      "node-head-1"
    ]
  },
  "validation": {
    "math_verified": false,
    "domain_verified": false,
    "verifier_used": "semantic_validator_phase4a",
    "flagged_issues": []
  },
  "source_metadata": {
    "provider": "google",
    "model": "gemini-3.5-flash-lite",
    "generation_time_ms": 5815,
    "prompt_version": "v1.0"
  }
};
