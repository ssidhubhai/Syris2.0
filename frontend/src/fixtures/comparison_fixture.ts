import { ExplanationDocument } from '@/types/explanation';

export const comparisonChemistryFixture: ExplanationDocument = {
  document_id: 'doc-p1-organic-sn1-sn2-003',
  session_id: 'sess-test-003',
  title: 'Comparison: S_N1 vs S_N2 Nucleophilic Substitution Mechanisms',
  intent: 'comparison',
  subject: 'chemistry',
  language: 'hinglish',
  nodes: [
    {
      id: 'node-head-comp',
      type: 'heading',
      content: {
        text: 'Mechanism Contrast: $S_N1$ (Unimolecular) vs $S_N2$ (Bimolecular)',
        level: 1,
      },
      importance: 'critical',
      layout_preference: 'full_width',
    },
    {
      id: 'node-text-comp-intro',
      type: 'text',
      content: {
        markdown: 'Haloalkanes me nucleophilic substitution do distinct pathways follow kar sakti hai: carbocation intermediate pathway ($S_N1$) ya concerted transition state pathway ($S_N2$). Inka competition substrate hindrance, nucleophile strength aur solvent polarity par depend karta hai.',
      },
      importance: 'supporting',
      layout_preference: 'full_width',
    },
    {
      id: 'node-comp-table',
      type: 'comparison',
      content: {
        title: 'Direct Mechanistic Comparison Matrix',
        left_title: 'S_N1 Pathway',
        left_points: [
          'Kinetics: Rate = $k [R-X]$ (First Order)',
          'Steps: Two-step mechanism via planar carbocation',
          'Stereochemistry: Racemization (with slight inversion)',
          'Substrate Preference: $3^\\circ > 2^\\circ \\gg 1^\\circ$',
          'Solvent: Polar Protic (e.g. $H_2O$, $ROH$ stabilize carbocation)',
        ],
        right_title: 'S_N2 Pathway',
        right_points: [
          'Kinetics: Rate = $k [R-X][Nu^-]$ (Second Order)',
          'Steps: Single concerted step with pentacoordinate transition state',
          'Stereochemistry: 100% Walden Inversion',
          'Substrate Preference: $\\text{Methyl} > 1^\\circ > 2^\\circ \\gg 3^\\circ$',
          'Solvent: Polar Aprotic (e.g. DMSO, DMF, Acetone)',
        ],
      },
      importance: 'critical',
      layout_preference: 'full_width',
    },
    {
      id: 'node-callout-solvolysis',
      type: 'callout',
      content: {
        callout_type: 'tip',
        title: 'JEE Advanced Decision Rule',
        markdown: 'Secondary ($2^\\circ$) alkyl halide ke case me: agar strong anionic nucleophile ($CN^-, SH^-, I^-$) with polar aprotic solvent hai toh **$S_N2$** dominant hoga; agar weak neutral nucleophile ($H_2O, EtOH$) with polar protic solvent hai toh **$S_N1$** dominant hoga.',
      },
      importance: 'critical',
      layout_preference: 'full_width',
    },
  ],
  relationships: [
    {
      from: 'node-text-comp-intro',
      to: 'node-comp-table',
      type: 'explains',
      label: 'Matrix breakdown',
    },
    {
      from: 'node-comp-table',
      to: 'node-callout-solvolysis',
      type: 'highlights',
      label: 'Secondary substrate bifurcation',
    },
  ],
  validation: {
    math_verified: false,
    domain_verified: false,
    verifier_used: 'not_run_static_fixture',
    flagged_issues: [],
  },
  source_metadata: {
    provider: 'static_mock_phase1',
    model: 'handcrafted_comparison_v1',
    generation_time_ms: 0,
  },
};
