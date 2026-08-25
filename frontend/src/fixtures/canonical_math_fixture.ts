import { ExplanationDocument } from '@/types/explanation';

export const canonicalMathFixture: ExplanationDocument = {
  document_id: 'doc-m1-calculus-feynman-001',
  session_id: 'sess-math-001',
  title: "Evaluation of Frullani-Type Definite Integral via Feynman's Trick",
  intent: 'derivation_proof',
  subject: 'mathematics',
  language: 'hinglish',
  nodes: [
    {
      id: 'node-math-head',
      type: 'heading',
      content: {
        text: 'Evaluating $\\int_0^\\infty \\frac{e^{-x} - e^{-ax}}{x} dx$ using Parameter Differentiation',
        level: 1,
      },
      importance: 'critical',
      layout_preference: 'full_width',
    },
    {
      id: 'node-math-intro',
      type: 'text',
      content: {
        markdown: 'Direct integration of this non-elementary integrand is difficult because of the $1/x$ denominator singularity at $x=0$. Hum parameter $a > 0$ introduce karke **Differentiation Under the Integral Sign (Leibniz Rule)** apply karenge.',
      },
      importance: 'supporting',
      layout_preference: 'full_width',
    },
    {
      id: 'node-math-def',
      type: 'definition',
      content: {
        title: 'Parametric Integral Definition',
        latex: 'I(a) = \\int_0^\\infty \\frac{e^{-x} - e^{-ax}}{x} \, dx \quad (a > 0)',
        annotation: 'Notice the boundary condition: $I(1) = \\int_0^\\infty 0 \, dx = 0$',
      },
      importance: 'critical',
      layout_preference: 'sticky_context',
    },
    {
      id: 'node-math-step1',
      type: 'derivation_step',
      content: {
        step_number: 1,
        title: 'Differentiate with Respect to Parameter $a$',
        explanation: 'Integral ke andar partial derivative $\\frac{\\partial}{\\partial a}$ apply karte hain. Denominator $x$ cancel ho jayega:',
        latex: "I'(a) = \\frac{d}{da} \\int_0^\\infty \\frac{e^{-x} - e^{-ax}}{x} \, dx = \\int_0^\\infty \\frac{\\partial}{\\partial a} \\left( \\frac{e^{-x} - e^{-ax}}{x} \\right) dx",
      },
      importance: 'critical',
      layout_preference: 'split_left',
    },
    {
      id: 'node-math-step2',
      type: 'derivation_step',
      content: {
        step_number: 2,
        title: 'Evaluate the Standard Exponential Integral',
        explanation: 'Partial derivative gives $\\frac{-(-x e^{-ax})}{x} = e^{-ax}$. Ab standard definite integral evaluate karte hain:',
        latex: "I'(a) = \\int_0^\\infty e^{-ax} \, dx = \\left[ \\frac{e^{-ax}}{-a} \\right]_0^\\infty = 0 - \\left(-\\frac{1}{a}\\right) = \\frac{1}{a}",
      },
      importance: 'critical',
      layout_preference: 'split_left',
    },
    {
      id: 'node-math-step3',
      type: 'derivation_step',
      content: {
        step_number: 3,
        title: 'Integrate Back with Initial Condition',
        explanation: "$I'(a) = 1/a$ ko integrate karke boundary condition $I(1) = 0$ substitute karte hain:",
        latex: 'I(a) = \\int \\frac{1}{a} \, da = \\ln|a| + C \implies I(1) = \\ln(1) + C = 0 \implies C = 0',
      },
      importance: 'critical',
      layout_preference: 'split_left',
    },
    {
      id: 'node-math-callout',
      type: 'callout',
      content: {
        callout_type: 'tip',
        title: 'JEE Shortcut: Frullani Integral Formula',
        markdown: 'Whenever you see $\\int_0^\\infty \\frac{f(ax) - f(bx)}{x} dx$ where $f(\\infty)$ exists, the direct answer is always $[f(0) - f(\\infty)] \\ln(b/a)$. Here $f(x) = e^{-x} \\implies (1 - 0)\\ln(a/1) = \\ln a$.',
      },
      importance: 'supporting',
      layout_preference: 'split_right',
    },
    {
      id: 'node-math-conclusion',
      type: 'conclusion',
      content: {
        title: 'Final Closed-Form Result',
        latex: '\\int_0^\\infty \\frac{e^{-x} - e^{-ax}}{x} \, dx = \\ln(a) \quad \forall \; a > 0',
        highlight: true,
      },
      importance: 'critical',
      layout_preference: 'full_width',
    },
  ],
  relationships: [
    {
      from: 'node-math-def',
      to: 'node-math-step1',
      type: 'defines',
      label: 'Differentiate parametric definition',
    },
    {
      from: 'node-math-step1',
      to: 'node-math-step2',
      type: 'derives_from',
      label: 'Cancel denominator x',
    },
    {
      from: 'node-math-step2',
      to: 'node-math-step3',
      type: 'derives_from',
      label: 'Integrate dI/da = 1/a',
    },
    {
      from: 'node-math-step3',
      to: 'node-math-conclusion',
      type: 'derives_from',
      label: 'Final integral value',
    },
    {
      from: 'node-math-conclusion',
      to: 'node-math-callout',
      type: 'highlights',
      label: 'Frullani verification',
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
    model: 'handcrafted_canonical_math_v1',
    generation_time_ms: 0,
  },
};
