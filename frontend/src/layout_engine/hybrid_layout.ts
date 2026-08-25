import { ExplanationDocument, ExplanationNode, Relationship } from '@/types/explanation';
import { CompositionEngine } from './composition_engine';
import { CompositionPlan, CompositionGroup } from '@/types/composition';

export interface PartitionedLayout {
  plan: CompositionPlan;
  nodeMap: Map<string, ExplanationNode>;
  relationships: Relationship[];
}

export function partitionDocumentLayout(
  doc: ExplanationDocument
): PartitionedLayout {
  const plan = CompositionEngine.planComposition(doc);
  const nodeMap = new Map<string, ExplanationNode>();
  for (const node of doc.nodes) {
    nodeMap.set(node.id, node);
  }

  return {
    plan,
    nodeMap,
    relationships: doc.relationships,
  };
}

export function getNodeRelationships(nodeId: string, relationships: Relationship[]) {
  const outgoing = relationships.filter((r) => r.from === nodeId);
  const incoming = relationships.filter((r) => r.to === nodeId);
  const relatedNodeIds = Array.from(
    new Set([...outgoing.map((r) => r.to), ...incoming.map((r) => r.from)])
  );

  return {
    outgoing,
    incoming,
    relatedNodeIds,
  };
}
