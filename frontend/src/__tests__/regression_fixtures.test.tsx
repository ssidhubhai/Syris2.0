import React from 'react';
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { ExplanationDocument } from '@/types/explanation';
import { CompositionEngine } from '@/layout_engine/composition_engine';
import { partitionDocumentLayout } from '@/layout_engine/hybrid_layout';
import { DigitalPaperCanvas } from '@/components/digital_paper/DigitalPaperCanvas';
import { REGRESSION_FIXTURES, REGRESSION_METADATA } from '@/fixtures/regression';

describe('Phase 4C Real-AI Regression Fixtures Suite', () => {
  it('should have all 8 frozen real-AI regression fixtures registered', () => {
    expect(REGRESSION_METADATA).toHaveLength(8);
    expect(Object.keys(REGRESSION_FIXTURES)).toHaveLength(8);
  });

  for (const meta of REGRESSION_METADATA) {
    describe(`Regression Case: ${meta.id} (${meta.title})`, () => {
      const doc: ExplanationDocument = REGRESSION_FIXTURES[meta.id];

      it('should strictly conform to ExplanationDocument structure', () => {
        expect(doc.document_id).toBeDefined();
        expect(doc.session_id).toBeDefined();
        expect(doc.title).toBeDefined();
        expect(doc.subject).toBeDefined();
        expect(doc.nodes.length).toBeGreaterThan(0);
        expect(doc.relationships).toBeDefined();
        expect(doc.validation).toBeDefined();
        expect(doc.source_metadata).toBeDefined();
      });

      it('should generate a deterministic CompositionPlan without crashing', () => {
        const plan = CompositionEngine.planComposition(doc);

        expect(plan).toBeDefined();
        expect(plan.pattern).toBeDefined();
        expect(plan.groups.length).toBeGreaterThan(0);
      });

      it('should partition document layout with 100% referential integrity', () => {
        const layout = partitionDocumentLayout(doc);

        expect(layout.nodeMap.size).toBe(doc.nodes.length);
        for (const rel of doc.relationships) {
          expect(layout.nodeMap.has(rel.from)).toBe(true);
          expect(layout.nodeMap.has(rel.to)).toBe(true);
        }
      });

      it('should render <DigitalPaperCanvas> cleanly in the DOM', () => {
        const { container } = render(
          <DigitalPaperCanvas
            document={doc}
            zoomScale={1.0}
            focusedNodeId={null}
            onFocusNode={() => {}}
            targetNodeId={null}
            onJumpToReference={() => {}}
          />
        );

        expect(container).toBeDefined();
        expect(container.querySelector('[data-testid="digital-paper-canvas"]')).not.toBeNull();
      });
    });
  }
});
