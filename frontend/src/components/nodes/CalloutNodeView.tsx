import React from 'react';
import { CalloutNodeContent } from '@/types/explanation';
import { InlineMarkdown } from '../digital_paper/InlineMarkdown';
import { AlertCircle } from 'lucide-react';

interface CalloutNodeViewProps {
  content: CalloutNodeContent;
  onJump?: (nodeId: string) => void;
}

export const CalloutNodeView: React.FC<CalloutNodeViewProps> = ({ content, onJump }) => {
  return (
    <div className="my-4 pl-3.5 py-2 border-l-2 border-amber-600/80 bg-amber-50/30 rounded-r text-ink-900">
      <div className="text-xs font-mono font-bold uppercase tracking-wider text-amber-900 mb-1">
        <InlineMarkdown content={content.title} onJump={onJump} />
      </div>
      <div className="text-xs sm:text-sm text-ink-800 leading-relaxed font-sans">
        <InlineMarkdown content={content.markdown} onJump={onJump} />
      </div>
    </div>
  );
};
