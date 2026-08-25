import { ExplanationDocument } from '@/types/explanation';

export const compactPhysicsFixture: ExplanationDocument = {
  document_id: 'doc-p1-mechanics-centripetal-004',
  session_id: 'sess-test-004',
  title: 'Definition of Centripetal Acceleration',
  intent: 'definition',
  subject: 'physics',
  language: 'hinglish',
  nodes: [
    {
      id: 'node-head-compact',
      type: 'heading',
      content: {
        text: 'Centripetal Acceleration ($a_c$)',
        level: 1,
      },
      importance: 'critical',
      layout_preference: 'full_width',
    },
    {
      id: 'node-text-compact',
      type: 'text',
      content: {
        markdown: 'Uniform circular motion me speed constant rehti hai par velocity vector ki direction continuously change hoti rehti hai. Is direction change ki wajah se circle ke center ki taraf directed acceleration ko **centripetal acceleration** kehte hain.',
      },
      importance: 'critical',
      layout_preference: 'full_width',
    },
    {
      id: 'node-def-centripetal',
      type: 'definition',
      content: {
        title: 'Centripetal Acceleration Formula',
        latex: 'a_c = \\frac{v^2}{R} = \\omega^2 R',
        annotation: 'Direction is always radial toward the center of curvature.',
      },
      importance: 'critical',
      layout_preference: 'full_width',
    },
  ],
  relationships: [],
  validation: {
    math_verified: false,
    domain_verified: false,
    verifier_used: 'not_run_static_fixture',
    flagged_issues: [],
  },
  source_metadata: {
    provider: 'static_mock_phase1',
    model: 'handcrafted_compact_v1',
    generation_time_ms: 0,
  },
};
