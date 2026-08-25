import React from 'react';
import { ExplanationNode } from '@/types/explanation';
import { HeadingNodeView } from '../nodes/HeadingNodeView';
import { TextNodeView } from '../nodes/TextNodeView';
import { DefinitionNodeView } from '../nodes/DefinitionNodeView';
import { EquationNodeView } from '../nodes/EquationNodeView';
import { DerivationStepView } from '../nodes/DerivationStepView';
import { ComparisonNodeView } from '../nodes/ComparisonNodeView';
import { ConclusionNodeView } from '../nodes/ConclusionNodeView';
import { CalloutNodeView } from '../nodes/CalloutNodeView';
import { DiagramNodeView } from '../nodes/DiagramNodeView';

interface NodeContainerProps {
  node: ExplanationNode;
  onJump?: (nodeId: string) => void;
  onHover?: (nodeId: string | null) => void;
  onClick?: (nodeId: string) => void;
  isTarget?: boolean;
  isFocused?: boolean;
  isRelated?: boolean;
  isDimmed?: boolean;
}

export const NodeContainer: React.FC<NodeContainerProps> = ({
  node,
  onJump,
  onHover,
  onClick,
  isTarget = false,
  isFocused = false,
  isRelated = false,
  isDimmed = false,
}) => {
  return (
    <div
      id={node.id}
      data-node-id={node.id}
      data-node-type={node.type}
      onMouseEnter={() => onHover?.(node.id)}
      onMouseLeave={() => onHover?.(null)}
      onClick={() => onClick?.(node.id)}
      className={`node-paper-block relative transition-all duration-300 rounded-lg ${
        isTarget
          ? 'ring-3 ring-academic-chem-accent shadow-paper-glow-target bg-amber-50/30'
          : isFocused
          ? 'ring-2 ring-academic-physics-accent shadow-paper-glow bg-blue-50/20'
          : isRelated
          ? 'ring-1 ring-academic-physics-border'
          : ''
      } ${isDimmed ? 'opacity-30 grayscale-[30%]' : 'opacity-100'}`}
    >
      {renderNodeContent(node, onJump)}
    </div>
  );
};

function renderNodeContent(node: ExplanationNode, onJump?: (nodeId: string) => void) {
  switch (node.type) {
    case 'heading':
      return <HeadingNodeView content={node.content} onJump={onJump} />;
    case 'text':
      return <TextNodeView content={node.content} onJump={onJump} />;
    case 'definition':
      return <DefinitionNodeView content={node.content} onJump={onJump} />;
    case 'equation':
      return <EquationNodeView content={node.content} />;
    case 'derivation_step':
      return <DerivationStepView content={node.content} onJump={onJump} />;
    case 'comparison':
      return <ComparisonNodeView content={node.content} onJump={onJump} />;
    case 'conclusion':
      return <ConclusionNodeView content={node.content} />;
    case 'callout':
      return <CalloutNodeView content={node.content} onJump={onJump} />;
    case 'diagram':
      return <DiagramNodeView content={node.content} />;
    default:
      return (
        <div className="p-3 bg-paper-100 rounded text-ink-700 text-sm">
          {JSON.stringify(node.content)}
        </div>
      );
  }
}
