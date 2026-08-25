import React from 'react';
import { HeadingNodeContent } from '@/types/explanation';
import { InlineMarkdown } from '../digital_paper/InlineMarkdown';

interface HeadingNodeViewProps {
  content: HeadingNodeContent;
  onJump?: (nodeId: string) => void;
}

export const HeadingNodeView: React.FC<HeadingNodeViewProps> = ({ content, onJump }) => {
  return (
    <div className="pb-3 mb-2 border-b border-paper-300">
      <div className="flex items-center gap-2 mb-1.5 font-mono text-xs text-ink-500">
        <span className="font-bold text-academic-physics-ink uppercase tracking-wider">
          [ Academic Solution Sheet ]
        </span>
      </div>
      <h1 className="text-xl sm:text-2xl font-serif font-bold text-ink-900 tracking-tight leading-snug">
        <InlineMarkdown content={content.text} onJump={onJump} />
      </h1>
    </div>
  );
};
