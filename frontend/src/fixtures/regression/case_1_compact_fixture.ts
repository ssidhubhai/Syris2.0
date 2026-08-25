import { ExplanationDocument } from '@/types/explanation';

/**
 * Frozen Real-AI Regression Fixture for Phase 4C
 * Case: Centripetal Acceleration Definition (compact)
 * Query: "What is centripetal acceleration? Define it and state its magnitude and directional relationship with velocity vector."
 * Model: gemini-3.5-flash-lite | Prompt: v1.0
 */
export const case_1_compact_fixture: ExplanationDocument = {
  "document_id": "doc-0df91b42",
  "session_id": "sess-p4c-73bdd1f7",
  "title": "Centripetal Acceleration",
  "intent": "definition",
  "subject": "physics",
  "language": "english",
  "nodes": [
    {
      "id": "node-head-1",
      "type": "heading",
      "content": {
        "text": "Centripetal Acceleration",
        "level": 1
      },
      "importance": "critical",
      "layout_preference": "auto"
    },
    {
      "id": "node-def-1",
      "type": "definition",
      "content": {
        "title": "Centripetal Acceleration Definition",
        "latex": "a_c = \\frac{v^2}{r} = \\omega^2 r",
        "annotation": "The acceleration experienced by an object moving in a circular path, directed towards the center of the curvature."
      },
      "importance": "critical",
      "layout_preference": "auto"
    },
    {
      "id": "node-text-1",
      "type": "text",
      "content": {
        "markdown": "Even if an object moves at a constant speed $v$ along a circular path of radius $r$, its velocity vector is continuously changing direction. This change in direction gives rise to an acceleration known as centripetal acceleration."
      },
      "importance": "supporting",
      "layout_preference": "auto"
    },
    {
      "id": "node-eq-1",
      "type": "equation",
      "content": {
        "latex": "Magnitude of Centripetal Acceleration",
        "id_tag": "Eq. (1)",
        "label": "Magnitude of Centripetal Acceleration",
        "purpose": "core formula expression for centripetal acceleration in terms of linear speed and radius or angular velocity and radius"
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
        "callout_type": "info",
        "purpose": "Directional relationship clarification for JEE aspirants"
      },
      "importance": "critical",
      "layout_preference": "auto"
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
      "to": "node-eq-1",
      "type": "uses"
    },
    {
      "from": "node-eq-1",
      "to": "node-callout-1",
      "type": "highlights"
    }
  ],
  "layout_hints": {
    "recommended_layout": "auto"
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
    "generation_time_ms": 3749,
    "prompt_version": "v1.0"
  }
};
