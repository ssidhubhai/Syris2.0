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
    <div className="my-3 py-3 px-4 bg-academic-physics-bg/50 border-l-3 border-academic-physics-accent rounded-r-md text-ink-900">
      <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-academic-physics-ink mb-1 font-mono">
        <Bookmark className="w-3.5 h-3.5 text-academic-physics-accent" />
        <span>{content.title}</span>
      </div>
      {content.latex && (
        <div className="py-2 text-center overflow-x-auto text-base sm:text-lg">
          <KaTeXMath math={content.latex} displayMode={true} />
        </div>
      )}
      {content.annotation && (
        <div className="text-xs text-ink-600 mt-1 font-mono">
          <InlineMarkdown content={content.annotation} onJump={onJump} />
        </div>
      )}
    </div>
  );
};
