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
    <div className="my-4 py-3 px-4 bg-[#FAF9F5] border border-[#E5E3D8] rounded-lg text-ink-800" data-testid="diagram-node-view">
      <div className="pb-1.5 mb-2 border-b border-[#E5E3D8]/60 text-xs font-mono font-bold text-ink-700 uppercase tracking-wide">
        {content.title || 'System Diagram'}
      </div>
      <p className="text-sm text-ink-700 leading-relaxed font-sans">
        {content.purpose || 'Visual model representing physical constraints and coordinates.'}
      </p>
    </div>
  );
};
