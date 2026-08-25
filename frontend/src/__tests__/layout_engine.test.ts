import { describe, it, expect } from 'vitest';
import { canonicalPhysicsFixture } from '@/fixtures/canonical_physics_fixture';
import { partitionDocumentLayout, getNodeRelationships } from '@/layout_engine/hybrid_layout';

describe('Hybrid Layout Engine with Composition Plan', () => {
  it('should build a nodeMap and composition plan for the document', () => {
    const layout = partitionDocumentLayout(canonicalPhysicsFixture);
    expect(layout.plan).toBeDefined();
    expect(layout.nodeMap.size).toBe(canonicalPhysicsFixture.nodes.length);
    expect(layout.relationships).toEqual(canonicalPhysicsFixture.relationships);
  });

  it('should extract correct incoming, outgoing, and related node IDs', () => {
    const normalEqRels = getNodeRelationships('node-eq-normal', canonicalPhysicsFixture.relationships);
    expect(normalEqRels.incoming.map((r) => r.from)).toContain('node-diag-fbd');
    expect(normalEqRels.outgoing.map((r) => r.to)).toContain('node-deriv-substitute');
  });
});
