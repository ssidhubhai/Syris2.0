import { ExplanationDocument } from '@/types/explanation';

/**
 * Frozen Real-AI Regression Fixture for Phase 4C
 * Case: Apparent Weight in Accelerating Lift (Hinglish) (hinglish)
 * Query: "Bhai mechanics me jab lift upward accelerate hoti hai toh apparent weight kyu increase hota hai? Normal reaction aur pseudo force se samjhao."
 * Model: gemini-3.5-flash-lite | Prompt: v1.0
 */
export const case_6_hinglish_lift_fixture: ExplanationDocument = {
  "document_id": "doc-68afeb7a",
  "session_id": "sess-p4c-35eb9e3c",
  "title": "Apparent Weight in an Accelerating Lift",
  "intent": "concept_explanation",
  "subject": "physics",
  "language": "hinglish",
  "nodes": [
    {
      "id": "node-head-1",
      "type": "heading",
      "content": {
        "text": "Apparent Weight in an Accelerating Lift",
        "level": 1
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-text-1",
      "type": "text",
      "content": {
        "markdown": "Jab lift upward accelerate karti hai, toh hamein apna weight thoda zyada (heavy) feel hota hai. Isko Newton ke laws aur Non-Inertial Frame (Pseudo Force) dono methods se analyze kar sakte hain."
      },
      "importance": "supporting",
      "layout_preference": "auto"
    },
    {
      "id": "node-def-1",
      "type": "definition",
      "content": {
        "title": "Apparent Weight",
        "latex": "W_{app} = N",
        "annotation": "Apparent weight is actually the normal reaction force (N) exerted by the floor on the person."
      },
      "importance": "critical",
      "layout_preference": "split_left"
    },
    {
      "id": "node-eq-1",
      "type": "equation",
      "content": {
        "latex": "Ground Frame (Inertial Frame) Analysis",
        "id_tag": "Eq. (1)",
        "label": "Ground Frame (Inertial Frame) Analysis",
        "explanation": "Let mass of person be m, upward acceleration be a, and normal reaction be N. Net force equation in upward direction:"
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-deriv-1",
      "type": "derivation_step",
      "content": {
        "latex": "Applying Newton's Second Law in the upward direction inside the ground reference frame:",
        "step_number": 1,
        "explanation": "Applying Newton's Second Law in the upward direction inside the ground reference frame:"
      },
      "importance": "critical",
      "layout_preference": "auto"
    },
    {
      "id": "node-eq-2",
      "type": "equation",
      "content": {
        "latex": "Equation of Motion",
        "id_tag": "Eq. (2)",
        "label": "Equation of Motion"
      },
      "importance": "critical",
      "layout_preference": "auto"
    },
    {
      "id": "node-deriv-2",
      "type": "derivation_step",
      "content": {
        "latex": "Normal reaction N ki value nikalne ke liye mg ko right side shift karte hain:",
        "step_number": 2,
        "explanation": "Normal reaction N ki value nikalne ke liye mg ko right side shift karte hain:"
      },
      "importance": "critical",
      "layout_preference": "auto"
    },
    {
      "id": "node-callout-1",
      "type": "callout",
      "content": {
        "markdown": "Important concept regarding info.",
        "title": "info",
        "callout_type": "info"
      },
      "importance": "note",
      "layout_preference": "full_width"
    },
    {
      "id": "node-conc-1",
      "type": "conclusion",
      "content": {
        "title": "Final Result",
        "highlight": true
      },
      "importance": "critical",
      "layout_preference": "full_width"
    }
  ],
  "relationships": [
    {
      "from": "node-def-1",
      "to": "node-eq-1",
      "type": "defines",
      "label": "Apparent weight defined as N"
    },
    {
      "from": "node-eq-1",
      "to": "node-deriv-1",
      "type": "substitutes_into",
      "label": "Setup Newton's Law"
    },
    {
      "from": "node-deriv-1",
      "to": "node-eq-2",
      "type": "derives_from",
      "label": "Formulate equation"
    },
    {
      "from": "node-eq-2",
      "to": "node-deriv-2",
      "type": "transforms_into",
      "label": "Isolate N"
    },
    {
      "from": "node-deriv-2",
      "to": "node-conc-1",
      "type": "derives_from",
      "label": "Final expression"
    },
    {
      "from": "node-conc-1",
      "to": "node-callout-1",
      "type": "highlights",
      "label": "Pseudo-force perspective"
    }
  ],
  "layout_hints": {
    "recommended_layout": "vertical_flow",
    "primary_channel_nodes": [
      "node-head-1",
      "node-text-1",
      "node-eq-1",
      "node-deriv-1",
      "node-eq-2",
      "node-deriv-2",
      "node-conc-1"
    ],
    "context_channel_nodes": [
      "node-def-1",
      "node-callout-1"
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
    "generation_time_ms": 4829,
    "prompt_version": "v1.0"
  }
};
