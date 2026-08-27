import React from 'react';
import { HeadingNodeContent } from '@/types/explanation';
import { InlineMarkdown } from '../digital_paper/InlineMarkdown';

interface HeadingNodeViewProps {
  content: HeadingNodeContent;
  onJump?: (nodeId: string) => void;
}

export const HeadingNodeView: React.FC<HeadingNodeViewProps> = ({ content, onJump }) => {
  if (content.level === 1) {
    return (
      <div className="pb-4 mb-5 border-b border-[#E8E5DC]">
        <h1 className="text-2xl sm:text-3xl font-serif font-bold text-ink-900 tracking-tight leading-snug">
          <InlineMarkdown content={content.text} onJump={onJump} />
        </h1>
      </div>
    );
  }

  return (
    <div className="pt-4 pb-2 mb-3 border-b border-[#E8E5DC]/60">
      <h2 className="text-lg sm:text-xl font-serif font-bold text-ink-900 tracking-tight leading-snug">
        <InlineMarkdown content={content.text} onJump={onJump} />
      </h2>
    </div>
  );
};
