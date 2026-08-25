import { ExplanationDocument } from '@/types/explanation';

export const canonicalChemFixture: ExplanationDocument = {
  document_id: 'doc-c1-organic-sn1-sn2-001',
  session_id: 'sess-chem-001',
  title: 'Bimolecular ($S_N2$) vs Unimolecular ($S_N1$) Nucleophilic Substitution',
  intent: 'comparison_mechanism',
  subject: 'chemistry',
  language: 'hinglish',
  nodes: [
    {
      id: 'node-chem-head',
      type: 'heading',
      content: {
        text: 'Deciding Between $S_N1$ and $S_N2$ Mechanisms in Alkyl Halides',
        level: 1,
      },
      importance: 'critical',
      layout_preference: 'full_width',
    },
    {
      id: 'node-chem-intro',
      type: 'text',
      content: {
        markdown: 'Substrate structure, nucleophile strength, and solvent polarity decide ki reaction unimolecular two-step carbocation pathway ($S_N1$) se jayegi ya single-step concerted backside attack ($S_N2$) se.',
      },
      importance: 'supporting',
      layout_preference: 'full_width',
    },
    {
      id: 'node-chem-gov',
      type: 'definition',
      content: {
        title: 'Governing Rate Laws',
        latex: '\\text{Rate}_{S_N2} = k_2 [R-X][Nu^-] \quad \text{vs} \quad \text{Rate}_{S_N1} = k_1 [R-X]',
        annotation: '$S_N2$ depends on nucleophile concentration; $S_N1$ is independent of nucleophile strength.',
      },
      importance: 'critical',
      layout_preference: 'sticky_context',
    },
    {
      id: 'node-chem-step1',
      type: 'derivation_step',
      content: {
        step_number: 1,
        title: 'Substrate Steric Hindrance & Carbocation Stability',
        explanation: 'Primary ($1^\\circ$) alkyl halides minimize transition-state sterics for backside attack ($S_N2$). Tertiary ($3^\\circ$) alkyl halides form stable planar carbocations ($S_N1$):',
        latex: '3^\\circ > 2^\\circ > 1^\\circ \; (S_N1 \text{ Rate}) \quad \longleftrightarrow \quad 1^\\circ > 2^\\circ > 3^\\circ \; (S_N2 \text{ Rate})',
      },
      importance: 'critical',
      layout_preference: 'split_left',
    },
    {
      id: 'node-chem-step2',
      type: 'derivation_step',
      content: {
        step_number: 2,
        title: 'Stereochemical Consequence: Inversion vs Racemization',
        explanation: '$S_N2$ gives 100% Walden Inversion (backside attack). $S_N1$ forms planar $sp^2$ carbocation allowing attack from front and back:',
        latex: 'S_N2 \implies \text{Complete Inversion of Configuration} \qquad S_N1 \implies \text{Racemization + Partial Inversion}',
      },
      importance: 'critical',
      layout_preference: 'split_left',
    },
    {
      id: 'node-chem-callout',
      type: 'callout',
      content: {
        callout_type: 'trap',
        title: 'Kota Trap: Polar Protic vs Aprotic Solvents',
        markdown: 'Polar Protic solvents (Water, EtOH) solvate nucleophiles via H-bonding, favoring $S_N1$. Polar Aprotic solvents (DMSO, DMF, Acetone) leave nucleophiles "naked" and highly reactive, strongly speeding up $S_N2$ by factors of $10^4$!',
      },
      importance: 'supporting',
      layout_preference: 'split_right',
    },
    {
      id: 'node-chem-conclusion',
      type: 'conclusion',
      content: {
        title: 'Decision Matrix Rule of Thumb',
        latex: '\\text{Strong Nu}^- + \\text{Polar Aprotic} + 1^\\circ/2^\\circ \implies S_N2 \qquad \text{Weak Nu} + \\text{Polar Protic} + 3^\\circ \implies S_N1',
        highlight: true,
      },
      importance: 'critical',
      layout_preference: 'full_width',
    },
  ],
  relationships: [
    {
      from: 'node-chem-gov',
      to: 'node-chem-step1',
      type: 'explains',
      label: 'Kinetic order determines mechanism pathway',
    },
    {
      from: 'node-chem-step1',
      to: 'node-chem-step2',
      type: 'causes',
      label: 'Mechanism geometry dictates stereochemistry',
    },
    {
      from: 'node-chem-step2',
      to: 'node-chem-conclusion',
      type: 'derives_from',
      label: 'Synthesis of decision matrix',
    },
    {
      from: 'node-chem-conclusion',
      to: 'node-chem-callout',
      type: 'highlights',
      label: 'Solvent effect warning',
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
    model: 'handcrafted_canonical_chem_v1',
    generation_time_ms: 0,
  },
};
