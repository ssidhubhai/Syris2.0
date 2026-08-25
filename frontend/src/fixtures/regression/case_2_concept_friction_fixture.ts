import { ExplanationDocument } from '@/types/explanation';

/**
 * Frozen Real-AI Regression Fixture for Phase 4C
 * Case: Microscopic Origin of Relative Friction (conceptual)
 * Query: "Why does friction oppose the tendency of relative motion rather than absolute motion? Explain microscopic interlocking and relative velocity."
 * Model: gemini-3.5-flash-lite | Prompt: v1.0
 */
export const case_2_concept_friction_fixture: ExplanationDocument = {
  "document_id": "doc-74f3046e",
  "session_id": "sess-p4c-11f728c8",
  "title": "Why Friction Opposes Relative Motion (Not Absolute Motion)",
  "intent": "concept_explanation",
  "subject": "physics",
  "language": "english",
  "nodes": [
    {
      "id": "node-head-1",
      "type": "heading",
      "content": {
        "text": "Why Friction Opposes Relative Motion",
        "level": 1
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-def-1",
      "type": "definition",
      "content": {
        "title": "Frictional Force Definition",
        "latex": "f_{\text{friction}} \\propto \\text{Relative Velocity or Tendency}",
        "annotation": "Friction always acts parallel to the contact surfaces to oppose relative motion or the tendency of relative motion between two bodies in contact."
      },
      "importance": "critical",
      "layout_preference": "auto"
    },
    {
      "id": "node-text-1",
      "type": "text",
      "content": {
        "markdown": "A common misconception is that friction opposes absolute motion. If friction opposed absolute motion, any object on the surface of the Earth would experience a massive retarding force because the Earth is spinning on its axis and orbiting the Sun at tremendous speeds! In reality, friction only cares about the **relative motion** between the two surfaces directly in contact."
      },
      "importance": "critical",
      "layout_preference": "auto"
    },
    {
      "id": "node-head-2",
      "type": "heading",
      "content": {
        "text": "Microscopic Interlocking and Cold-Welding",
        "level": 2
      },
      "importance": "supporting",
      "layout_preference": "full_width"
    },
    {
      "id": "node-text-2",
      "type": "text",
      "content": {
        "markdown": "On a microscopic level, no surface is perfectly flat. They possess microscopic irregularities called **asperities**. When two surfaces are pressed together, actual physical contact occurs only at the tips of these asperities. Under high local pressure, microscopic bonds or 'cold welds' form at these contact points.\n\nWhen one body tries to slide relative to the other, these microscopic interlocking bumps and adhesive bonds must be sheared or lifted over each other. This resistance to relative displacement is what macroscopic friction manifests as."
      },
      "importance": "supporting",
      "layout_preference": "auto"
    },
    {
      "id": "node-eq-1",
      "type": "equation",
      "content": {
        "latex": "Maximum Static Friction",
        "id_tag": "Eq. (1)",
        "label": "Maximum Static Friction",
        "explanation": "Governed by the normal force and coefficient of static friction.",
        "purpose": "quantify threshold limit before relative motion begins"
      },
      "importance": "critical",
      "layout_preference": "auto"
    },
    {
      "id": "node-callout-1",
      "type": "callout",
      "content": {
        "markdown": "Important concept regarding trap.",
        "title": "trap",
        "callout_type": "trap"
      },
      "importance": "critical",
      "layout_preference": "auto"
    },
    {
      "id": "node-conc-1",
      "type": "conclusion",
      "content": {
        "title": "Core Takeaway",
        "latex": "\\vec{f} \\parallel \\vec{v}_{1/2}",
        "highlight": true
      },
      "importance": "critical",
      "layout_preference": "full_width"
    }
  ],
  "relationships": [
    {
      "from": "node-head-1",
      "to": "node-def-1",
      "type": "defines"
    },
    {
      "from": "node-def-1",
      "to": "node-text-1",
      "type": "explains"
    },
    {
      "from": "node-text-1",
      "to": "node-head-2",
      "type": "follows_from"
    },
    {
      "from": "node-head-2",
      "to": "node-text-2",
      "type": "explains"
    },
    {
      "from": "node-text-2",
      "to": "node-eq-1",
      "type": "uses"
    },
    {
      "from": "node-eq-1",
      "to": "node-callout-1",
      "type": "highlights"
    },
    {
      "from": "node-callout-1",
      "to": "node-conc-1",
      "type": "derives_from"
    }
  ],
  "layout_hints": {
    "recommended_layout": "vertical_flow",
    "primary_channel_nodes": [
      "node-head-1",
      "node-def-1",
      "node-text-1",
      "node-head-2",
      "node-text-2",
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
    "generation_time_ms": 6547,
    "prompt_version": "v1.0"
  }
};
