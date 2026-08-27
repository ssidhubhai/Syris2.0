import React from 'react';
import { EquationNodeContent } from '@/types/explanation';
import { KaTeXMath } from '../digital_paper/KaTeXMath';

interface EquationNodeViewProps {
  content: EquationNodeContent;
}

export const EquationNodeView: React.FC<EquationNodeViewProps> = ({ content }) => {
  return (
    <div className="my-3 py-1.5 flex items-center justify-between gap-3 group">
      <div className="flex-1 text-center overflow-x-auto text-base sm:text-lg text-ink-900 py-1">
        <KaTeXMath math={content.latex} displayMode={true} />
      </div>
      {(content.id_tag || content.label) && (
        <div className="shrink-0 text-right font-mono text-xs text-ink-500 select-none flex items-center gap-1.5">
          {content.label && (
            <span className="text-[11px] text-ink-400 font-sans italic hidden sm:inline">
              {content.label}
            </span>
          )}
          {content.id_tag && (
            <span className="font-semibold text-ink-700 bg-paper-200/60 px-1.5 py-0.5 rounded text-[11px]">
              {content.id_tag}
            </span>
          )}
        </div>
      )}
    </div>
  );
};
