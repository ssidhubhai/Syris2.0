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
    <div className="my-6 py-4 px-2 border-y border-[#D5D2C7] bg-[#FAF9F5]/80 rounded text-ink-900">
      <div className="text-xs font-mono font-bold uppercase tracking-wider text-ink-800 mb-2">
        <InlineMarkdown content={content.title} />
      </div>
      <div className="py-2 text-center overflow-x-auto text-lg sm:text-xl font-medium text-ink-950">
        <KaTeXMath math={content.latex} displayMode={true} />
      </div>
    </div>
  );
};
