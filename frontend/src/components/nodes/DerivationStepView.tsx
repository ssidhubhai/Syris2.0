import React from 'react';
import { DerivationStepContent } from '@/types/explanation';
import { KaTeXMath } from '../digital_paper/KaTeXMath';
import { InlineMarkdown } from '../digital_paper/InlineMarkdown';

interface DerivationStepViewProps {
  content: DerivationStepContent;
  onJump?: (nodeId: string) => void;
}

export const DerivationStepView: React.FC<DerivationStepViewProps> = ({ content, onJump }) => {
  const isDuplicate =
    content.latex &&
    (content.latex.trim() === (content.explanation || '').trim() ||
     content.latex.trim() === (content.title || '').trim());

  return (
    <div className="my-3 pl-4 border-l-2 border-academic-physics-border relative group">
      <div className="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-paper-50 border-2 border-academic-physics-accent flex items-center justify-center text-[10px] font-bold text-academic-physics-ink">
        {content.step_number}
      </div>

      {content.title && (
        <div className="text-xs font-bold uppercase tracking-wider text-ink-700 font-mono mb-1">
          <InlineMarkdown content={content.title} onJump={onJump} />
        </div>
      )}

      {content.explanation && (
        <div className="text-sm text-ink-700 mb-2 leading-relaxed">
          <InlineMarkdown content={content.explanation} onJump={onJump} />
        </div>
      )}

      {content.latex && !isDuplicate && (
        <div className="py-2 px-3 bg-paper-100/40 rounded text-center overflow-x-auto text-sm sm:text-base border border-paper-200/50">
          <KaTeXMath math={content.latex} displayMode={true} />
        </div>
      )}
    </div>
  );
};
