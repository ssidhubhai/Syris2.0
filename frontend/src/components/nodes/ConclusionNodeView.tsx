import React from 'react';
import { ConclusionNodeContent } from '@/types/explanation';
import { KaTeXMath } from '../digital_paper/KaTeXMath';
import { InlineMarkdown } from '../digital_paper/InlineMarkdown';
import { Check } from 'lucide-react';

interface ConclusionNodeViewProps {
  content: ConclusionNodeContent;
}

export const ConclusionNodeView: React.FC<ConclusionNodeViewProps> = ({ content }) => {
  return (
    <div className="my-5 p-4 bg-emerald-50/40 border-y-2 border-emerald-500/80 rounded-md text-ink-900">
      <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-emerald-800 mb-2 font-mono">
        <Check className="w-4 h-4 text-emerald-600" />
        <span><InlineMarkdown content={content.title} /></span>
      </div>
      <div className="py-2 text-center overflow-x-auto text-base sm:text-lg font-semibold">
        <KaTeXMath math={content.latex} displayMode={true} />
      </div>
    </div>
  );
};
