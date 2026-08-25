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
    <div className="my-4 p-4 rounded-lg bg-[#FAF9F5] border border-paper-300 text-ink-900" data-testid="comparison-node-view">
      <div className="flex items-center gap-2 mb-3 pb-2 border-b border-paper-200">
        <GitCompare className="w-4 h-4 text-academic-chem-accent" />
        <h3 className="text-xs font-bold uppercase tracking-wider text-ink-800 font-mono">
          {content.title}
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Left Column */}
        <div className="p-3 bg-white rounded border border-paper-200">
          <div className="text-xs font-bold uppercase tracking-wider text-academic-physics-ink mb-2 pb-1 border-b border-paper-200 font-mono">
            {content.left_title}
          </div>
          <ul className="space-y-2 text-xs sm:text-sm text-ink-800">
            {content.left_points.map((pt, idx) => (
              <li key={idx} className="flex items-start gap-1.5">
                <span className="text-academic-physics-accent mt-0.5">•</span>
                <div>
                  <InlineMarkdown content={pt} onJump={onJump} />
                </div>
              </li>
            ))}
          </ul>
        </div>

        {/* Right Column */}
        <div className="p-3 bg-white rounded border border-paper-200">
          <div className="text-xs font-bold uppercase tracking-wider text-academic-chem-ink mb-2 pb-1 border-b border-paper-200 font-mono">
            {content.right_title}
          </div>
          <ul className="space-y-2 text-xs sm:text-sm text-ink-800">
            {content.right_points.map((pt, idx) => (
              <li key={idx} className="flex items-start gap-1.5">
                <span className="text-academic-chem-accent mt-0.5">•</span>
                <div>
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
