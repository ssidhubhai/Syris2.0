import React from 'react';
import { EquationNodeContent } from '@/types/explanation';
import { KaTeXMath } from '../digital_paper/KaTeXMath';

interface EquationNodeViewProps {
  content: EquationNodeContent;
}

export const EquationNodeView: React.FC<EquationNodeViewProps> = ({ content }) => {
  return (
    <div className="my-2 py-2 px-3 rounded-md hover:bg-paper-100/50 transition-colors border-b border-paper-200/60">
      <div className="flex items-center justify-between text-xs text-ink-500 font-mono mb-1">
        <span className="font-semibold">{content.label || 'Governing Equation'}</span>
        {content.id_tag && (
          <span className="font-bold text-academic-physics-ink bg-academic-physics-bg px-2 py-0.5 rounded border border-academic-physics-border/60">
            {content.id_tag}
          </span>
        )}
      </div>
      <div className="py-1 text-center overflow-x-auto text-sm sm:text-base">
        <KaTeXMath math={content.latex} displayMode={true} />
      </div>
    </div>
  );
};
