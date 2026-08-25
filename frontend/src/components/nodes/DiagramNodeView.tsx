import React from 'react';
import { DiagramNodeContent } from '@/types/whiteboard';
import { PhysicsCanvas2D } from '../whiteboard/PhysicsCanvas2D';

interface DiagramNodeViewProps {
  content: DiagramNodeContent;
}

export const DiagramNodeView: React.FC<DiagramNodeViewProps> = ({ content }) => {
  if (content.canvas_type === 'PHYSICS_2D') {
    return <PhysicsCanvas2D content={content} />;
  }

  return (
    <div className="p-4 bg-[#FAF9F5] border border-paper-300/90 rounded-xl text-ink-800 shadow-xs" data-testid="diagram-node-view">
      <div className="flex items-center justify-between pb-2 mb-2 border-b border-paper-200 text-xs font-mono">
        <span className="font-bold text-ink-700 uppercase tracking-wide">
          {content.title || 'System Diagram'}
        </span>
        <span className="text-[11px] font-semibold text-academic-physics-ink bg-academic-physics-bg px-2 py-0.5 rounded border border-academic-physics-border/50">
          Conceptual Visual
        </span>
      </div>
      <p className="text-sm text-ink-700 leading-relaxed font-sans">
        {content.purpose || 'Visual model representing physical constraints and coordinates.'}
      </p>
    </div>
  );
};
