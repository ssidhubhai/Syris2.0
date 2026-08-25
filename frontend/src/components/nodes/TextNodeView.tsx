import React from 'react';
import { TextNodeContent } from '@/types/explanation';
import { InlineMarkdown } from '../digital_paper/InlineMarkdown';

interface TextNodeViewProps {
  content: TextNodeContent;
  onJump?: (nodeId: string) => void;
}

export const TextNodeView: React.FC<TextNodeViewProps> = ({ content, onJump }) => {
  return (
    <div className="text-sm sm:text-base leading-relaxed text-ink-800 my-2">
      <InlineMarkdown content={content.markdown} onJump={onJump} />
    </div>
  );
};
