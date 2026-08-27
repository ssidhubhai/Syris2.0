import React, { useEffect, useState } from 'react';
import { Relationship } from '@/types/explanation';
import { calculateBezierConnector, ConnectorCurve } from '@/layout_engine/connector_routing';

interface RelationshipOverlayProps {
  relationships: Relationship[];
  activeSourceId: string | null;
  activeTargetId: string | null;
  containerRef: React.RefObject<HTMLDivElement | null>;
}

export const RelationshipOverlay: React.FC<RelationshipOverlayProps> = ({
  relationships,
  activeSourceId,
  activeTargetId,
  containerRef,
}) => {
  const [curves, setCurves] = useState<{ rel: Relationship; curve: ConnectorCurve }[]>([]);

  useEffect(() => {
    if (!containerRef.current) return;
    const container = containerRef.current;
    const containerRect = container.getBoundingClientRect();

    const activeRels = relationships.filter(
      (r) =>
        r.from === activeSourceId ||
        r.to === activeSourceId ||
        r.from === activeTargetId ||
        r.to === activeTargetId
    );

    const calculated: { rel: Relationship; curve: ConnectorCurve }[] = [];

    for (const rel of activeRels) {
      const fromEl = container.querySelector(`[data-node-id="${rel.from}"]`);
      const toEl = container.querySelector(`[data-node-id="${rel.to}"]`);

      if (fromEl && toEl) {
        const fromRect = fromEl.getBoundingClientRect();
        const toRect = toEl.getBoundingClientRect();
        const curve = calculateBezierConnector(fromRect, toRect, containerRect);
        calculated.push({ rel, curve });
      }
    }

    setCurves(calculated);
  }, [relationships, activeSourceId, activeTargetId, containerRef]);

  if (curves.length === 0) return null;

  return (
    <svg
      className="absolute inset-0 pointer-events-none z-20 w-full h-full"
      style={{ overflow: 'visible' }}
      data-testid="relationship-overlay"
    >
      <defs>
        <marker
          id="rel-arrow"
          viewBox="0 0 10 10"
          refX="6"
          refY="5"
          markerWidth="5"
          markerHeight="5"
          orient="auto-start-reverse"
        >
          <path d="M 0 2 L 8 5 L 0 8 z" fill="#0284C7" />
        </marker>
      </defs>

      {curves.map(({ rel, curve }, idx) => (
        <g key={idx} className="animate-fadeIn">
          <path
            d={curve.path}
            fill="none"
            stroke="#0284C7"
            strokeWidth="1.5"
            strokeDasharray="4 3"
            markerEnd="url(#rel-arrow)"
            opacity="0.85"
          />
          <circle cx={curve.start.x} cy={curve.start.y} r="3" fill="#0284C7" opacity="0.85" />
          <circle cx={curve.end.x} cy={curve.end.y} r="3" fill="#0284C7" opacity="0.85" />

          {rel.label && (
            <g transform={`translate(${curve.labelPosition.x}, ${curve.labelPosition.y})`}>
              <rect
                x="-36"
                y="-8"
                width="72"
                height="16"
                rx="8"
                fill="#F0F9FF"
                stroke="#BAE0FD"
                strokeWidth="1"
              />
              <text
                x="0"
                y="3"
                textAnchor="middle"
                fontSize="9"
                fontFamily="monospace"
                fontWeight="600"
                fill="#0369A1"
              >
                {rel.type}
              </text>
            </g>
          )}
        </g>
      ))}
    </svg>
  );
};
