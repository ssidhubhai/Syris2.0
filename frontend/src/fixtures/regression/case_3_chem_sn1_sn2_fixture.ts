import { ExplanationDocument } from '@/types/explanation';

/**
 * Frozen Real-AI Regression Fixture for Phase 4C
 * Case: SN1 vs SN2 Mechanisms Comparison (comparison)
 * Query: "What is the difference between SN1 and SN2 reaction mechanisms in organic chemistry? Compare kinetics, intermediate, solvent, and stereochemistry."
 * Model: gemini-3.5-flash-lite | Prompt: v1.0
 */
export const case_3_chem_sn1_sn2_fixture: ExplanationDocument = {
  "document_id": "doc-584a7108",
  "session_id": "sess-p4c-01faf4ae",
  "title": "Comparison of SN1 and SN2 Reaction Mechanisms",
  "intent": "comparison",
  "subject": "chemistry",
  "language": "english",
  "nodes": [
    {
      "id": "node-head-1",
      "type": "heading",
      "content": {
        "text": "Nucleophilic Substitution Mechanisms: SN1 vs SN2",
        "level": 1
      },
      "importance": "critical",
      "layout_preference": "full_width"
    },
    {
      "id": "node-def-sn1",
      "type": "definition",
      "content": {
        "title": "SN1 Mechanism (Substitution Nucleophilic Unimolecular)",
        "latex": "\\text{Rate} = k[R-X]",
        "annotation": "Two-step process involving a planar carbocation intermediate."
      },
      "importance": "critical",
      "layout_preference": "auto"
    },
    {
      "id": "node-def-sn2",
      "type": "definition",
      "content": {
        "title": "SN2 Mechanism (Substitution Nucleophilic Bimolecular)",
        "latex": "\\text{Rate} = k[R-X][\\text{Nu}^-]",
        "annotation": "Concerted single-step process with a pentavalent transition state and Walden inversion."
      },
      "importance": "critical",
      "layout_preference": "auto"
    },
    {
      "id": "node-comp-1",
      "type": "comparison",
      "content": {
        "title": "Comprehensive Feature Comparison",
        "left_title": "SN1 Mechanism",
        "left_points": [
          "Kinetics: First-order overall (Rate = k[Substrate])",
          "Intermediate: Stable planar carbocation",
          "Solvent: Polar protic solvents stabilize carbocation",
          "Stereochemistry: Racemization (mixture of inversion and retention)"
        ],
        "right_title": "SN2 Mechanism",
        "right_points": [
          "Kinetics: Second-order overall (Rate = k[Substrate][Nucleophile])",
          "Intermediate: No intermediate (concerted transition state)",
          "Solvent: Polar aprotic solvents enhance nucleophile strength",
          "Stereochemistry: Complete inversion of configuration (Walden Inversion)"
        ]
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
        "callout_type": "trap",
        "purpose": "Common JEE Trap regarding substrate steric hindrance and carbocation rearrangement stability in SN1/SN2 questions."
      },
      "importance": "note",
      "layout_preference": "full_width"
    }
  ],
  "relationships": [
    {
      "from": "node-head-1",
      "to": "node-def-sn1",
      "type": "explains"
    },
    {
      "from": "node-head-1",
      "to": "node-def-sn2",
      "type": "explains"
    },
    {
      "from": "node-def-sn1",
      "to": "node-comp-1",
      "type": "contrasts_with"
    },
    {
      "from": "node-def-sn2",
      "to": "node-comp-1",
      "type": "contrasts_with"
    },
    {
      "from": "node-comp-1",
      "to": "node-callout-1",
      "type": "highlights"
    }
  ],
  "layout_hints": {
    "recommended_layout": "split_columns"
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
    "generation_time_ms": 3940,
    "prompt_version": "v1.0"
  }
};
