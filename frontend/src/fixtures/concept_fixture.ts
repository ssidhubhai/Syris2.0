import { ExplanationDocument } from '@/types/explanation';

export const conceptPhysicsFixture: ExplanationDocument = {
  document_id: 'doc-p1-electro-potential-002',
  session_id: 'sess-test-002',
  title: 'Why Electric Potential is a Scalar Quantity',
  intent: 'conceptual_explanation',
  subject: 'physics',
  language: 'hinglish',
  nodes: [
    {
      id: 'node-head-concept',
      type: 'heading',
      content: {
        text: 'Physical Origin of Electric Potential as a Scalar',
        level: 1,
      },
      importance: 'critical',
      layout_preference: 'full_width',
    },
    {
      id: 'node-text-concept-1',
      type: 'text',
      content: {
        markdown: 'Electric potential $V$ conservative electrostatic field me **work done per unit test charge** represent karta hai. Work done khud force aur displacement ka dot product ($\\vec{F} \\cdot d\\vec{r}$) hone ki wajah se ek **scalar quantity** hota hai, isliye potential ke paas koi spatial direction nahi hoti.',
      },
      importance: 'critical',
      layout_preference: 'full_width',
    },
    {
      id: 'node-def-work',
      type: 'definition',
      content: {
        title: 'Fundamental Line Integral Definition',
        latex: 'V(r) = -\\int_{\\infty}^{r} \\vec{E} \\cdot d\\vec{r}',
        annotation: 'Dot product $\\vec{E} \\cdot d\\vec{r}$ ensures the resulting quantity is invariant under coordinate rotation.',
      },
      importance: 'critical',
      layout_preference: 'full_width',
    },
    {
      id: 'node-text-superposition',
      type: 'text',
      content: {
        markdown: 'Jab multiple point charges present hote hain, toh net electric potential simply **algebraic sum** (with sign) hota hai, jabki electric field ke liye vector addition (parallelogram law) use karna padta hai.',
      },
      importance: 'supporting',
      layout_preference: 'full_width',
    },
    {
      id: 'node-eq-superposition',
      type: 'equation',
      content: {
        id_tag: 'Superposition',
        label: 'Scalar Algebraic Superposition',
        latex: 'V_{\\text{net}} = \\sum_{i=1}^n \\frac{k q_i}{r_i} = \\frac{k q_1}{r_1} + \\frac{k q_2}{r_2} + \\dots',
      },
      importance: 'critical',
      layout_preference: 'full_width',
    },
    {
      id: 'node-conclusion-concept',
      type: 'conclusion',
      content: {
        title: 'Key Pedagogical Invariant',
        latex: '\\vec{E} = -\\vec{\\nabla} V \\quad \\iff \\quad \\text{Field is directional gradient of scalar potential}',
        highlight: true,
      },
      importance: 'critical',
      layout_preference: 'full_width',
    },
  ],
  relationships: [
    {
      from: 'node-def-work',
      to: 'node-eq-superposition',
      type: 'derives_from',
      label: 'Linearity of line integral',
    },
    {
      from: 'node-eq-superposition',
      to: 'node-conclusion-concept',
      type: 'explains',
      label: 'Gradient relationship',
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
    model: 'handcrafted_concept_v1',
    generation_time_ms: 0,
  },
};
