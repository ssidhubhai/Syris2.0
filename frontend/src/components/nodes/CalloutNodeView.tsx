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
    <div className="my-3 p-3 bg-amber-50/70 border-l-3 border-amber-500 rounded-r-md text-ink-900 shadow-paper-sm">
      <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-amber-900 mb-1 font-mono">
        <AlertCircle className="w-3.5 h-3.5 text-amber-600" />
        <span><InlineMarkdown content={content.title} onJump={onJump} /></span>
      </div>
      <div className="text-xs sm:text-sm text-ink-800 leading-relaxed">
        <InlineMarkdown content={content.markdown} onJump={onJump} />
      </div>
    </div>
  );
};
