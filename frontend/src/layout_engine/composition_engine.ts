import { ExplanationDocument, ExplanationNode } from '@/types/explanation';
import { CompositionPlan, CompositionPattern, CompositionGroup } from '@/types/composition';

export class CompositionEngine {
  public static planComposition(doc: ExplanationDocument): CompositionPlan {
    const pattern = this.determinePattern(doc);

    const headerNodes: ExplanationNode[] = [];
    const stickyNodes: ExplanationNode[] = [];
    const mainBodyNodes: ExplanationNode[] = [];
    const visualNodes: ExplanationNode[] = [];
    const equationNodes: ExplanationNode[] = [];
    const derivationNodes: ExplanationNode[] = [];
    const comparisonNodes: ExplanationNode[] = [];
    const marginaliaNodes: ExplanationNode[] = [];
    const synthesisNodes: ExplanationNode[] = [];

    for (const node of doc.nodes) {
      if (node.type === 'heading' || (node.type === 'text' && node.id.includes('intro'))) {
        headerNodes.push(node);
      } else if (node.layout_preference === 'sticky_context') {
        stickyNodes.push(node);
      } else if (node.type === 'diagram' || node.type === 'graph') {
        visualNodes.push(node);
      } else if (node.type === 'equation') {
        equationNodes.push(node);
      } else if (node.type === 'derivation_step') {
        derivationNodes.push(node);
      } else if (node.type === 'comparison') {
        comparisonNodes.push(node);
      } else if (node.type === 'callout') {
        marginaliaNodes.push(node);
      } else if (node.type === 'conclusion') {
        synthesisNodes.push(node);
      } else {
        mainBodyNodes.push(node);
      }
    }

    const headerGroup: CompositionGroup | undefined =
      headerNodes.length > 0
        ? {
            id: 'group-header',
            node_ids: headerNodes.map((n) => n.id),
            arrangement: 'vertical_flow',
            semantic_role: 'primary',
            priority: 100,
          }
        : undefined;

    const stickyContextGroup: CompositionGroup | undefined =
      stickyNodes.length > 0
        ? {
            id: 'group-sticky-context',
            node_ids: stickyNodes.map((n) => n.id),
            arrangement: 'emphasis_block',
            semantic_role: 'context',
            priority: 90,
          }
        : undefined;

    const groups: CompositionGroup[] = [];

    if (pattern === 'DIAGRAM_CENTRIC') {
      const visualPlacement = visualNodes.length > 0 ? 'right' : 'inline';
      const pairedNodeIds = [
        ...visualNodes.map((n) => n.id),
        ...equationNodes.map((n) => n.id),
        ...derivationNodes.map((n) => n.id),
        ...marginaliaNodes.map((n) => n.id),
      ];

      groups.push({
        id: 'group-diagram-derivation-pair',
        node_ids: pairedNodeIds,
        arrangement: 'visual_with_explanation',
        semantic_role: 'primary',
        priority: 80,
        layout_hint: {
          split_ratio: 'balanced',
          visual_placement: visualPlacement,
          collapse_behavior: 'stack',
        },
      });
    } else if (pattern === 'COMPARISON') {
      groups.push({
        id: 'group-comparison-main',
        node_ids: comparisonNodes.map((n) => n.id),
        arrangement: 'comparison_columns',
        semantic_role: 'primary',
        priority: 80,
      });

      if (marginaliaNodes.length > 0) {
        groups.push({
          id: 'group-comparison-notes',
          node_ids: marginaliaNodes.map((n) => n.id),
          arrangement: 'vertical_flow',
          semantic_role: 'marginalia',
          priority: 70,
        });
      }
    } else if (pattern === 'DERIVATION_CENTRIC') {
      const derivationFlowIds = [
        ...mainBodyNodes.map((n) => n.id),
        ...equationNodes.map((n) => n.id),
        ...derivationNodes.map((n) => n.id),
      ];
      groups.push({
        id: 'group-derivation-flow',
        node_ids: derivationFlowIds,
        arrangement: 'vertical_flow',
        semantic_role: 'primary',
        priority: 80,
      });

      if (marginaliaNodes.length > 0) {
        groups.push({
          id: 'group-derivation-marginalia',
          node_ids: marginaliaNodes.map((n) => n.id),
          arrangement: 'vertical_flow',
          semantic_role: 'marginalia',
          priority: 70,
        });
      }
    } else if (pattern === 'COMPACT_EXPLANATION') {
      const compactNodeIds = [
        ...mainBodyNodes.map((n) => n.id),
        ...stickyNodes.map((n) => n.id),
        ...equationNodes.map((n) => n.id),
      ];
      groups.push({
        id: 'group-compact-body',
        node_ids: compactNodeIds,
        arrangement: 'vertical_flow',
        semantic_role: 'primary',
        priority: 80,
      });
    } else {
      // CONCEPT_CENTRIC or MIXED
      const conceptFlowIds = [
        ...mainBodyNodes.map((n) => n.id),
        ...stickyNodes.map((n) => n.id),
        ...equationNodes.map((n) => n.id),
        ...marginaliaNodes.map((n) => n.id),
      ];
      groups.push({
        id: 'group-concept-flow',
        node_ids: conceptFlowIds,
        arrangement: 'vertical_flow',
        semantic_role: 'primary',
        priority: 80,
      });
    }

    const synthesisGroup: CompositionGroup | undefined =
      synthesisNodes.length > 0
        ? {
            id: 'group-synthesis',
            node_ids: synthesisNodes.map((n) => n.id),
            arrangement: 'emphasis_block',
            semantic_role: 'synthesis',
            priority: 10,
          }
        : undefined;

    return {
      pattern,
      headerGroup,
      stickyContextGroup,
      groups,
      synthesisGroup,
    };
  }

  public static determinePattern(doc: ExplanationDocument): CompositionPattern {
    if (doc.nodes.length <= 3 && !doc.nodes.some((n) => n.type === 'derivation_step' || n.type === 'diagram')) {
      return 'COMPACT_EXPLANATION';
    }

    const hasComparison = doc.nodes.some((n) => n.type === 'comparison');
    if (hasComparison || doc.intent === 'comparison') {
      return 'COMPARISON';
    }

    const hasDiagram = doc.nodes.some((n) => n.type === 'diagram');
    const hasDerivation = doc.nodes.some((n) => n.type === 'derivation_step');

    if (hasDiagram && hasDerivation) {
      return 'DIAGRAM_CENTRIC';
    }

    if (hasDiagram && !hasDerivation) {
      return 'DIAGRAM_CENTRIC';
    }

    if (hasDerivation && !hasDiagram) {
      return 'DERIVATION_CENTRIC';
    }

    if (doc.intent === 'conceptual_explanation' || doc.intent === 'concept') {
      return 'CONCEPT_CENTRIC';
    }

    return 'MIXED_EXPLANATION';
  }
}
