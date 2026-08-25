import { ExplanationDocument } from '@/types/explanation';

/**
 * Frozen Real-AI Regression Fixture for Phase 4C
 * Case: Total Internal Reflection & Critical Angle (optics_spatial)
 * Query: "Explain Total Internal Reflection (TIR) at a denser-to-rarer medium interface and derive the critical angle condition \sin \theta_c = 1/n."
 * Model: gemini-3.5-flash-lite | Prompt: v1.0
 */
export const case_7_optics_tir_fixture: ExplanationDocument = {
  "document_id": "doc-b9f8b968",
  "session_id": "sess-p4c-1fc2c19f",
  "title": "Total Internal Reflection and Critical Angle Derivation",
  "intent": "derivation",
  "subject": "physics",
  "language": "english",
  "nodes": [
    {
      "id": "node-head-1",
      "type": "heading",
      "content": {
        "text": "Total Internal Reflection (TIR) and Critical Angle",
        "level": 1
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-def-1",
      "type": "definition",
      "content": {
        "title": "Total Internal Reflection",
        "latex": "I_r = 100\\% \\text{ reflection when } \\theta_1 > \\theta_c",
        "annotation": "Occurs when light travels from an optically denser medium to a rarer medium at an angle of incidence greater than the critical angle."
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-eq-snell",
      "type": "equation",
      "content": {
        "latex": "Snell's Law at Interface",
        "id_tag": "Eq. (1)",
        "label": "Snell's Law at Interface"
      },
      "importance": "critical",
      "layout_preference": "auto"
    },
    {
      "id": "node-deriv-1",
      "type": "derivation_step",
      "content": {
        "latex": "\\text{Step 1}",
        "step_number": 1,
        "explanation": "Algebraic derivation step 1"
      },
      "importance": "supporting",
      "layout_preference": "auto"
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
      "layout_preference": "auto"
    },
    {
      "id": "node-conc-1",
      "type": "conclusion",
      "content": {
        "title": "Critical Angle Formula",
        "latex": "\\sin \\theta_c = \\frac{n_2}{n_1} \\text{ (or } \\frac{1}{n} \\text{ if rarer medium is air)}",
        "highlight": true
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
    }
  ],
  "relationships": [
    {
      "from": "node-head-1",
      "to": "node-def-1",
      "type": "defines",
      "label": "introduces concept"
    },
    {
      "from": "node-def-1",
      "to": "node-eq-snell",
      "type": "uses",
      "label": "applies Snell's Law"
    },
    {
      "from": "node-eq-snell",
      "to": "node-deriv-1",
      "type": "substitutes_into",
      "label": "sets angle of refraction to 90 degrees"
    },
    {
      "from": "node-deriv-1",
      "to": "node-deriv-2",
      "type": "derives_from",
      "label": "simplifies equation algebraically"
    },
    {
      "from": "node-deriv-2",
      "to": "node-conc-1",
      "type": "derives_from",
      "label": "yields final condition"
    },
    {
      "from": "node-conc-1",
      "to": "node-callout-1",
      "type": "highlights",
      "label": "caveat for medium condition"
    }
  ],
  "layout_hints": {
    "recommended_layout": "vertical_flow",
    "primary_channel_nodes": [
      "node-head-1",
      "node-def-1",
      "node-eq-snell",
      "node-deriv-1",
      "node-deriv-2",
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
    "generation_time_ms": 4256,
    "prompt_version": "v1.0"
  }
};
