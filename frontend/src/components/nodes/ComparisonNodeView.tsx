import React from 'react';
import { ComparisonNodeContent } from '@/types/explanation';
import { InlineMarkdown } from '../digital_paper/InlineMarkdown';
import { GitCompare } from 'lucide-react';

interface ComparisonNodeViewProps {
  content: ComparisonNodeContent;
  onJump?: (nodeId: string) => void;
}

export const ComparisonNodeView: React.FC<ComparisonNodeViewProps> = ({ content, onJump }) => {
  return (
    <div className="my-6 py-2 text-ink-900" data-testid="comparison-node-view">
      <div className="text-xs font-mono font-bold uppercase tracking-wider text-ink-700 pb-2 mb-4 border-b border-[#E5E3D8]">
        {content.title}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Left Column */}
        <div className="md:pr-4 md:border-r md:border-[#E5E3D8]/80">
          <h3 className="text-sm font-mono font-bold text-ink-900 mb-3 pb-1 border-b border-[#E5E3D8]/50">
            {content.left_title}
          </h3>
          <ul className="space-y-2 text-sm text-ink-800 leading-relaxed font-sans">
            {content.left_points.map((pt, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-ink-400 font-bold select-none">•</span>
                <div className="flex-1">
                  <InlineMarkdown content={pt} onJump={onJump} />
                </div>
              </li>
            ))}
          </ul>
        </div>

        {/* Right Column */}
        <div className="md:pl-2">
          <h3 className="text-sm font-mono font-bold text-ink-900 mb-3 pb-1 border-b border-[#E5E3D8]/50">
            {content.right_title}
          </h3>
          <ul className="space-y-2 text-sm text-ink-800 leading-relaxed font-sans">
            {content.right_points.map((pt, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-ink-400 font-bold select-none">•</span>
                <div className="flex-1">
                  <InlineMarkdown content={pt} onJump={onJump} />
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
