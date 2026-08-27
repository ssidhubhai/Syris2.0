import React from 'react';
import { ExplanationNode } from '@/types/explanation';
import { KaTeXMath } from './KaTeXMath';
import { Pin, ArrowUpRight } from 'lucide-react';

interface StickyContextBarProps {
  stickyNodes: ExplanationNode[];
  onJump: (nodeId: string) => void;
  visible: boolean;
}

export const StickyContextBar: React.FC<StickyContextBarProps> = ({
  stickyNodes,
  onJump,
  visible,
}) => {
  if (!visible || stickyNodes.length === 0) return null;

  const activeNode = stickyNodes[0];

  return (
    <div
      className="sticky top-0 z-30 w-full max-w-4xl bg-[#FDFCFB]/95 backdrop-blur-sm border-b border-[#E8E5DC] px-4 py-2 shadow-xs transition-all animate-fadeIn flex items-center justify-between"
      data-testid="sticky-context-bar"
    >
      <div className="flex items-center gap-3 overflow-hidden">
        <div className="flex items-center gap-1.5 text-xs font-mono font-bold uppercase tracking-wider text-ink-700 shrink-0">
          <Pin className="w-3.5 h-3.5 rotate-45 text-ink-500" />
          <span>Governing Principle:</span>
        </div>
        <div className="text-xs sm:text-sm font-sans text-ink-900 font-semibold truncate">
          {activeNode.content?.title}:
        </div>
        {activeNode.content?.latex && (
          <div className="px-2 py-0.5 bg-paper-100 rounded border border-[#E5E3D8] text-xs">
            <KaTeXMath math={activeNode.content.latex} displayMode={false} />
          </div>
        )}
      </div>

      <button
        type="button"
        onClick={() => onJump(activeNode.id)}
        className="shrink-0 flex items-center gap-1 text-xs font-mono font-medium text-ink-700 hover:text-ink-950 bg-paper-100 hover:bg-paper-200 px-2 py-1 rounded border border-[#E5E3D8] transition-colors"
      >
        <span>View in Context</span>
        <ArrowUpRight className="w-3 h-3" />
      </button>
    </div>
  );
};
