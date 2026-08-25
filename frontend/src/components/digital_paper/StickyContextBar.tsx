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
      className="sticky top-0 z-30 w-full bg-academic-physics-bg/95 backdrop-blur-sm border-b border-academic-physics-border px-4 py-2.5 shadow-paper-sm transition-all animate-fadeIn flex items-center justify-between"
      data-testid="sticky-context-bar"
    >
      <div className="flex items-center gap-3 overflow-hidden">
        <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-academic-physics-ink shrink-0">
          <Pin className="w-3.5 h-3.5 rotate-45 text-academic-physics-accent" />
          <span>Active Governing Law:</span>
        </div>
        <div className="text-xs sm:text-sm font-serif text-ink-900 font-bold truncate">
          {activeNode.content?.title}:
        </div>
        {activeNode.content?.latex && (
          <div className="px-2 py-0.5 bg-white rounded border border-academic-physics-border text-xs">
            <KaTeXMath math={activeNode.content.latex} displayMode={false} />
          </div>
        )}
      </div>

      <button
        type="button"
        onClick={() => onJump(activeNode.id)}
        className="shrink-0 flex items-center gap-1 text-xs font-semibold text-academic-physics-ink hover:text-academic-physics-accent bg-white/80 hover:bg-white px-2.5 py-1 rounded border border-academic-physics-border transition-colors shadow-sm"
      >
        <span>View In Law Card</span>
        <ArrowUpRight className="w-3 h-3" />
      </button>
    </div>
  );
};
