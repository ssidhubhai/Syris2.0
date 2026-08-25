import { canonicalPhysicsFixture } from './canonical_physics_fixture';
import { conceptPhysicsFixture } from './concept_fixture';
import { comparisonChemistryFixture } from './comparison_fixture';
import { compactPhysicsFixture } from './compact_fixture';
import { canonicalMathFixture } from './canonical_math_fixture';
import { ExplanationDocument } from '@/types/explanation';

export interface FixtureEntry {
  key: string;
  label: string;
  pattern: string;
  subject: 'physics' | 'chemistry' | 'mathematics' | 'general';
  sampleQuery: string;
  keywords: string[];
  doc: ExplanationDocument;
}

export const DEV_FIXTURES: Record<string, FixtureEntry> = {
  canonical_physics: {
    key: 'canonical_physics',
    label: 'Mechanics (FBD & Derivation)',
    pattern: 'DIAGRAM_CENTRIC',
    subject: 'physics',
    sampleQuery: 'Why is friction acting downward on the wedge?',
    keywords: ['friction', 'wedge', 'fbd', 'free body', 'block', 'incline', 'pseudo force', 'newton'],
    doc: canonicalPhysicsFixture,
  },
  concept_physics: {
    key: 'concept_physics',
    label: 'Electrostatics (Scalar Potential)',
    pattern: 'CONCEPT_CENTRIC',
    subject: 'physics',
    sampleQuery: 'Why is electric potential a scalar quantity?',
    keywords: ['electric potential', 'potential', 'scalar', 'electrostatics', 'conservative', 'gradient', 'line integral'],
    doc: conceptPhysicsFixture,
  },
  chemistry_comparison: {
    key: 'chemistry_comparison',
    label: 'Organic Chemistry (SN1 vs SN2)',
    pattern: 'COMPARISON',
    subject: 'chemistry',
    sampleQuery: 'How to decide between SN1 and SN2 mechanisms?',
    keywords: ['sn1', 'sn2', 'substitution', 'nucleophile', 'carbocation', 'walden', 'inversion', 'organic', 'solvent'],
    doc: comparisonChemistryFixture,
  },
  compact_definition: {
    key: 'compact_definition',
    label: 'Kinematics (Centripetal Acceleration)',
    pattern: 'COMPACT_EXPLANATION',
    subject: 'physics',
    sampleQuery: 'What is centripetal acceleration and how to derive it?',
    keywords: ['centripetal', 'centripetal acceleration', 'circular motion', 'radial', 'tangential', 'kinematics'],
    doc: compactPhysicsFixture,
  },
  canonical_math: {
    key: 'canonical_math',
    label: 'Calculus (Feynman Integral Technique)',
    pattern: 'DERIVATION_PROOF',
    subject: 'mathematics',
    sampleQuery: "Evaluate definite integral using Feynman's trick",
    keywords: ['integral', 'feynman', 'calculus', 'frullani', 'differentiation under integral', 'leibniz', 'math', 'maths'],
    doc: canonicalMathFixture,
  },
};

/**
 * Matches a user query string to one of the local demo fixtures based on keyword analysis.
 * Returns the matched FixtureEntry or null if no confident match is found.
 */
export function matchDemoFixture(query: string): FixtureEntry | null {
  const normalized = query.toLowerCase().trim();
  if (!normalized) return null;

  // Direct specific phrase mappings
  if (normalized.includes('friction') || normalized.includes('wedge')) {
    return DEV_FIXTURES.canonical_physics;
  }
  if (normalized.includes('potential') || normalized.includes('scalar') || normalized.includes('electrostat')) {
    return DEV_FIXTURES.concept_physics;
  }
  if (normalized.includes('sn1') || normalized.includes('sn2') || normalized.includes('substitut') || normalized.includes('chem')) {
    return DEV_FIXTURES.chemistry_comparison;
  }
  if (normalized.includes('centripetal') || normalized.includes('circular')) {
    return DEV_FIXTURES.compact_definition;
  }
  if (normalized.includes('feynman') || normalized.includes('integral') || normalized.includes('calculus') || normalized.includes('frullani') || normalized.includes('math')) {
    return DEV_FIXTURES.canonical_math;
  }

  // Keyword score fallback
  let bestEntry: FixtureEntry | null = null;
  let bestScore = 0;

  for (const entry of Object.values(DEV_FIXTURES)) {
    let score = 0;
    for (const keyword of entry.keywords) {
      if (normalized.includes(keyword)) {
        score += keyword.length;
      }
    }
    if (score > bestScore) {
      bestScore = score;
      bestEntry = entry;
    }
  }

  return bestScore > 0 ? bestEntry : null;
}
