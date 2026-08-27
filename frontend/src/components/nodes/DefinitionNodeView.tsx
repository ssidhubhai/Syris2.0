import React from 'react';
import { DefinitionNodeContent } from '@/types/explanation';
import { KaTeXMath } from '../digital_paper/KaTeXMath';
import { InlineMarkdown } from '../digital_paper/InlineMarkdown';
import { Bookmark } from 'lucide-react';

interface DefinitionNodeViewProps {
  content: DefinitionNodeContent;
  onJump?: (nodeId: string) => void;
}

export const DefinitionNodeView: React.FC<DefinitionNodeViewProps> = ({ content, onJump }) => {
  return (
    <div className="my-4 pl-4 py-1 border-l-2 border-ink-700 text-ink-900">
      <div className="text-xs font-mono font-bold uppercase tracking-wider text-ink-700 mb-1">
        {content.title}
      </div>
      {content.latex && (
        <div className="py-2 overflow-x-auto text-base sm:text-lg">
          <KaTeXMath math={content.latex} displayMode={true} />
        </div>
      )}
      {content.annotation && (
        <div className="text-xs text-ink-600 mt-1 italic font-sans">
          <InlineMarkdown content={content.annotation} onJump={onJump} />
        </div>
      )}
    </div>
  );
};
