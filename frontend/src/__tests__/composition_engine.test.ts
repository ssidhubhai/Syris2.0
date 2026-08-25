import { describe, it, expect } from 'vitest';
import { CompositionEngine } from '@/layout_engine/composition_engine';
import { canonicalPhysicsFixture } from '@/fixtures/canonical_physics_fixture';
import { conceptPhysicsFixture } from '@/fixtures/concept_fixture';
import { comparisonChemistryFixture } from '@/fixtures/comparison_fixture';
import { compactPhysicsFixture } from '@/fixtures/compact_fixture';

describe('CompositionEngine Semantic Strategies', () => {
  it('should classify spatial physics mechanics with FBD as DIAGRAM_CENTRIC', () => {
    const plan = CompositionEngine.planComposition(canonicalPhysicsFixture);
    expect(plan.pattern).toBe('DIAGRAM_CENTRIC');
    expect(plan.groups.some((g) => g.arrangement === 'visual_with_explanation')).toBe(true);
    expect(plan.headerGroup).toBeDefined();
    expect(plan.stickyContextGroup).toBeDefined();
    expect(plan.synthesisGroup).toBeDefined();
  });

  it('should classify conceptual electrostatic questions as CONCEPT_CENTRIC', () => {
    const plan = CompositionEngine.planComposition(conceptPhysicsFixture);
    expect(plan.pattern).toBe('CONCEPT_CENTRIC');
    expect(plan.groups.some((g) => g.arrangement === 'vertical_flow')).toBe(true);
    // Verifies no gratuitous diagram group is forced
    expect(plan.groups.some((g) => g.arrangement === 'visual_with_explanation')).toBe(false);
  });

  it('should classify reaction mechanism contrasts as COMPARISON', () => {
    const plan = CompositionEngine.planComposition(comparisonChemistryFixture);
    expect(plan.pattern).toBe('COMPARISON');
    expect(plan.groups.some((g) => g.arrangement === 'comparison_columns')).toBe(true);
  });

  it('should classify short definitional questions as COMPACT_EXPLANATION', () => {
    const plan = CompositionEngine.planComposition(compactPhysicsFixture);
    expect(plan.pattern).toBe('COMPACT_EXPLANATION');
    expect(plan.groups.length).toBe(1);
    expect(plan.groups[0].arrangement).toBe('vertical_flow');
  });

  it('should classify pure algebraic derivations without diagrams as DERIVATION_CENTRIC', () => {
    const pureDerivationDoc = {
      ...canonicalPhysicsFixture,
      document_id: 'doc-pure-derivation',
      nodes: canonicalPhysicsFixture.nodes.filter((n) => n.type !== 'diagram'),
    };
    const plan = CompositionEngine.planComposition(pureDerivationDoc);
    expect(plan.pattern).toBe('DERIVATION_CENTRIC');
    expect(plan.groups.some((g) => g.id === 'group-derivation-flow')).toBe(true);
  });
});
