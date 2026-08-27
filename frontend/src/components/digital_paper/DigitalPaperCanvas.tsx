import React, { useRef, useState, useEffect } from 'react';
import { ExplanationDocument, ExplanationNode } from '@/types/explanation';
import { partitionDocumentLayout, getNodeRelationships } from '@/layout_engine/hybrid_layout';
import { NodeContainer } from './NodeContainer';
import { StickyContextBar } from './StickyContextBar';
import { RelationshipOverlay } from './RelationshipOverlay';
import { CompositionGroup } from '@/types/composition';

interface DigitalPaperCanvasProps {
  document: ExplanationDocument;
  zoomScale: number;
  focusedNodeId: string | null;
  onFocusNode: (nodeId: string | null) => void;
  targetNodeId: string | null;
  onJumpToReference: (nodeId: string) => void;
}

export const DigitalPaperCanvas: React.FC<DigitalPaperCanvasProps> = ({
  document: doc,
  zoomScale,
  focusedNodeId,
  onFocusNode,
  targetNodeId,
  onJumpToReference,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null);
  const [isScrolled, setIsScrolled] = useState<boolean>(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 120);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const layout = partitionDocumentLayout(doc);
  const { plan, nodeMap } = layout;

  const activeHoverRelations = hoveredNodeId
    ? getNodeRelationships(hoveredNodeId, doc.relationships)
    : null;

  const activeFocusRelations = focusedNodeId
    ? getNodeRelationships(focusedNodeId, doc.relationships)
    : null;

  const relatedIds = Array.from(
    new Set([
      ...(activeHoverRelations?.relatedNodeIds || []),
      ...(activeFocusRelations?.relatedNodeIds || []),
    ])
  );

  const stickyNodes = plan.stickyContextGroup
    ? (plan.stickyContextGroup.node_ids.map((id) => nodeMap.get(id)).filter(Boolean) as ExplanationNode[])
    : [];

  return (
    <div className="relative w-full min-h-screen bg-[#F4F3EE] flex flex-col items-center py-4 sm:py-8 px-2 sm:px-6">
      <StickyContextBar
        stickyNodes={stickyNodes}
        onJump={onJumpToReference}
        visible={isScrolled}
      />

      <div
        ref={containerRef}
        style={{ transform: `scale(${zoomScale})`, transformOrigin: 'top center' }}
        className="relative w-full max-w-4xl bg-[#FDFCFB] p-6 sm:p-10 rounded-xl shadow-paper-md border border-[#E5E3D8] transition-transform duration-200"
        data-testid="digital-paper-canvas"
      >
        <RelationshipOverlay
          relationships={doc.relationships}
          activeSourceId={hoveredNodeId || focusedNodeId}
          activeTargetId={targetNodeId}
          containerRef={containerRef}
        />

        {/* 1. Header Group */}
        {plan.headerGroup && (
          <div className="space-y-2 mb-4">
            {plan.headerGroup.node_ids.map((id) => {
              const node = nodeMap.get(id);
              if (!node) return null;
              return (
                <NodeContainer
                  key={node.id}
                  node={node}
                  onJump={onJumpToReference}
                  onHover={setHoveredNodeId}
                  onClick={onFocusNode}
                  isTarget={targetNodeId === node.id}
                  isFocused={focusedNodeId === node.id}
                  isRelated={relatedIds.includes(node.id)}
                  isDimmed={Boolean(focusedNodeId && focusedNodeId !== node.id && !relatedIds.includes(node.id))}
                />
              );
            })}
          </div>
        )}

        {/* 2. Sticky Governing Context Group */}
        {plan.stickyContextGroup && (
          <div className="mb-4">
            {plan.stickyContextGroup.node_ids.map((id) => {
              const node = nodeMap.get(id);
              if (!node) return null;
              return (
                <NodeContainer
                  key={node.id}
                  node={node}
                  onJump={onJumpToReference}
                  onHover={setHoveredNodeId}
                  onClick={onFocusNode}
                  isTarget={targetNodeId === node.id}
                  isFocused={focusedNodeId === node.id}
                  isRelated={relatedIds.includes(node.id)}
                  isDimmed={Boolean(focusedNodeId && focusedNodeId !== node.id && !relatedIds.includes(node.id))}
                />
              );
            })}
          </div>
        )}

        {/* 3. Main Composition Groups */}
        <div className="space-y-6 mb-6">
          {plan.groups.map((group) => renderCompositionGroup(group, nodeMap, {
            onJump: onJumpToReference,
            onHover: setHoveredNodeId,
            onClick: onFocusNode,
            targetNodeId,
            focusedNodeId,
            relatedIds,
          }))}
        </div>

        {/* 4. Synthesis / Conclusion Group */}
        {plan.synthesisGroup && (
          <div className="space-y-3 pt-2 border-t border-paper-200">
            {plan.synthesisGroup.node_ids.map((id) => {
              const node = nodeMap.get(id);
              if (!node) return null;
              return (
                <NodeContainer
                  key={node.id}
                  node={node}
                  onJump={onJumpToReference}
                  onHover={setHoveredNodeId}
                  onClick={onFocusNode}
                  isTarget={targetNodeId === node.id}
                  isFocused={focusedNodeId === node.id}
                  isRelated={relatedIds.includes(node.id)}
                  isDimmed={Boolean(focusedNodeId && focusedNodeId !== node.id && !relatedIds.includes(node.id))}
                />
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

function renderCompositionGroup(
  group: CompositionGroup,
  nodeMap: Map<string, ExplanationNode>,
  handlers: {
    onJump: (id: string) => void;
    onHover: (id: string | null) => void;
    onClick: (id: string | null) => void;
    targetNodeId: string | null;
    focusedNodeId: string | null;
    relatedIds: string[];
  }
) {
  const nodes = group.node_ids.map((id) => nodeMap.get(id)).filter(Boolean) as ExplanationNode[];

  if (group.arrangement === 'visual_with_explanation') {
    const visualNodes = nodes.filter((n) => n.type === 'diagram' || n.type === 'graph');
    const derivationNodes = nodes.filter((n) => n.type !== 'diagram' && n.type !== 'graph' && n.type !== 'callout');
    const marginaliaNodes = nodes.filter((n) => n.type === 'callout');

    return (
      <div key={group.id} className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Visual & Marginalia Channel (Right on desktop, top on mobile) */}
        <div className="order-1 lg:order-2 lg:col-span-5 lg:sticky lg:top-14 space-y-4">
          {visualNodes.map((node) => (
            <NodeContainer
              key={node.id}
              node={node}
              onJump={handlers.onJump}
              onHover={handlers.onHover}
              onClick={handlers.onClick}
              isTarget={handlers.targetNodeId === node.id}
              isFocused={handlers.focusedNodeId === node.id}
              isRelated={handlers.relatedIds.includes(node.id)}
              isDimmed={Boolean(handlers.focusedNodeId && handlers.focusedNodeId !== node.id && !handlers.relatedIds.includes(node.id))}
            />
          ))}

          {marginaliaNodes.map((node) => (
            <NodeContainer
              key={node.id}
              node={node}
              onJump={handlers.onJump}
              onHover={handlers.onHover}
              onClick={handlers.onClick}
              isTarget={handlers.targetNodeId === node.id}
              isFocused={handlers.focusedNodeId === node.id}
              isRelated={handlers.relatedIds.includes(node.id)}
              isDimmed={Boolean(handlers.focusedNodeId && handlers.focusedNodeId !== node.id && !handlers.relatedIds.includes(node.id))}
            />
          ))}
        </div>

        {/* Primary Mathematical Channel (Left on desktop, bottom on mobile) */}
        <div className="order-2 lg:order-1 lg:col-span-7 space-y-2">
          {derivationNodes.map((node) => (
            <NodeContainer
              key={node.id}
              node={node}
              onJump={handlers.onJump}
              onHover={handlers.onHover}
              onClick={handlers.onClick}
              isTarget={handlers.targetNodeId === node.id}
              isFocused={handlers.focusedNodeId === node.id}
              isRelated={handlers.relatedIds.includes(node.id)}
              isDimmed={Boolean(handlers.focusedNodeId && handlers.focusedNodeId !== node.id && !handlers.relatedIds.includes(node.id))}
            />
          ))}
        </div>
      </div>
    );
  }

  // Default: vertical flow / comparison / inline
  return (
    <div key={group.id} className="space-y-3">
      {nodes.map((node) => (
        <NodeContainer
          key={node.id}
          node={node}
          onJump={handlers.onJump}
          onHover={handlers.onHover}
          onClick={handlers.onClick}
          isTarget={handlers.targetNodeId === node.id}
          isFocused={handlers.focusedNodeId === node.id}
          isRelated={handlers.relatedIds.includes(node.id)}
          isDimmed={Boolean(handlers.focusedNodeId && handlers.focusedNodeId !== node.id && !handlers.relatedIds.includes(node.id))}
        />
      ))}
    </div>
  );
}
