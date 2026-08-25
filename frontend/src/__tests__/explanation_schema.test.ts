import { describe, it, expect } from 'vitest';
import { canonicalPhysicsFixture } from '@/fixtures/canonical_physics_fixture';
import { conceptPhysicsFixture } from '@/fixtures/concept_fixture';
import { comparisonChemistryFixture } from '@/fixtures/comparison_fixture';
import { compactPhysicsFixture } from '@/fixtures/compact_fixture';
import { DEV_FIXTURES } from '@/fixtures';

describe('ExplanationDocument Schema Referential Integrity', () => {
  it('should have all dev fixtures registered in DEV_FIXTURES', () => {
    expect(Object.keys(DEV_FIXTURES)).toHaveLength(5);
    expect(DEV_FIXTURES.canonical_physics.pattern).toBe('DIAGRAM_CENTRIC');
    expect(DEV_FIXTURES.concept_physics.pattern).toBe('CONCEPT_CENTRIC');
    expect(DEV_FIXTURES.chemistry_comparison.pattern).toBe('COMPARISON');
    expect(DEV_FIXTURES.compact_definition.pattern).toBe('COMPACT_EXPLANATION');
  });

  it('should maintain referential integrity in canonical physics fixture', () => {
    const nodeIds = new Set(canonicalPhysicsFixture.nodes.map((n) => n.id));
    for (const rel of canonicalPhysicsFixture.relationships) {
      expect(nodeIds.has(rel.from)).toBe(true);
      expect(nodeIds.has(rel.to)).toBe(true);
    }
  });

  it('should maintain referential integrity in concept fixture', () => {
    const nodeIds = new Set(conceptPhysicsFixture.nodes.map((n) => n.id));
    for (const rel of conceptPhysicsFixture.relationships) {
      expect(nodeIds.has(rel.from)).toBe(true);
      expect(nodeIds.has(rel.to)).toBe(true);
    }
  });

  it('should maintain referential integrity in comparison fixture', () => {
    const nodeIds = new Set(comparisonChemistryFixture.nodes.map((n) => n.id));
    for (const rel of comparisonChemistryFixture.relationships) {
      expect(nodeIds.has(rel.from)).toBe(true);
      expect(nodeIds.has(rel.to)).toBe(true);
    }
  });
});
