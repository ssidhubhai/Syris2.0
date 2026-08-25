import { ExplanationDocument } from '@/types/explanation';

/**
 * Frozen Real-AI Regression Fixture for Phase 4C
 * Case: Integration by Parts Formula Derivation (derivation)
 * Query: "Derive the integration by parts formula \int u \, dv = uv - \int v \, du starting from the product rule of differentiation."
 * Model: gemini-3.5-flash-lite | Prompt: v1.0
 */
export const case_5_math_by_parts_fixture: ExplanationDocument = {
  "document_id": "doc-44394f24",
  "session_id": "sess-p4c-d60d43a4",
  "title": "Derivation of Integration by Parts Formula",
  "intent": "derivation",
  "subject": "mathematics",
  "language": "english",
  "nodes": [
    {
      "id": "node-head-1",
      "type": "heading",
      "content": {
        "text": "Derivation of Integration by Parts Formula",
        "level": 1
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-text-1",
      "type": "text",
      "content": {
        "markdown": "The integration by parts formula is a fundamental technique in integral calculus used for integrating products of functions. It originates directly from the product rule of differentiation."
      },
      "importance": "supporting",
      "layout_preference": "full_width"
    },
    {
      "id": "node-eq-1",
      "type": "equation",
      "content": {
        "latex": "Product Rule of Differentiation",
        "id_tag": "Eq. (1)",
        "label": "Product Rule of Differentiation"
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
      "id": "node-conc-1",
      "type": "conclusion",
      "content": {
        "title": "Integration by Parts Formula",
        "latex": "\\int u \\, dv = uv - \\int v \\, du",
        "highlight": true
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-callout-1",
      "type": "callout",
      "content": {
        "markdown": "Important concept regarding tip.",
        "title": "tip",
        "callout_type": "tip"
      },
      "importance": "note",
      "layout_preference": "full_width"
    }
  ],
  "relationships": [
    {
      "from": "node-head-1",
      "to": "node-text-1",
      "type": "follows_from"
    },
    {
      "from": "node-text-1",
      "to": "node-eq-1",
      "type": "uses"
    },
    {
      "from": "node-eq-1",
      "to": "node-deriv-1",
      "type": "substitutes_into"
    },
    {
      "from": "node-deriv-1",
      "to": "node-deriv-2",
      "type": "derives_from"
    },
    {
      "from": "node-deriv-2",
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
    "recommended_layout": "vertical_flow",
    "primary_channel_nodes": [
      "node-head-1",
      "node-text-1",
      "node-eq-1",
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
    "generation_time_ms": 3455,
    "prompt_version": "v1.0"
  }
};
