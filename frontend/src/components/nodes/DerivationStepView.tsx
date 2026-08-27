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
    <div className="my-4 pl-4 border-l-2 border-[#E5E3D8] hover:border-sky-400/80 transition-colors relative group">
      {/* Step Indicator Node */}
      <div className="flex items-center gap-2 mb-1.5">
        <span className="w-5 h-5 rounded-full bg-paper-100 border border-[#D5D2C7] flex items-center justify-center text-[10px] font-mono font-bold text-ink-700">
          <span>{content.step_number}</span>
        </span>
        {content.title && (
          <span className="text-xs font-mono font-bold uppercase tracking-wider text-ink-800">
            <InlineMarkdown content={content.title} onJump={onJump} />
          </span>
        )}
      </div>

      {content.explanation && (
        <div className="text-[14px] sm:text-[15px] text-ink-800 mb-2 leading-relaxed font-sans">
          <InlineMarkdown content={content.explanation} onJump={onJump} />
        </div>
      )}

      {content.latex && !isDuplicate && (
        <div className="py-2 text-center overflow-x-auto text-base sm:text-lg text-ink-900">
          <KaTeXMath math={content.latex} displayMode={true} />
        </div>
      )}
    </div>
  );
};
