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
          markerWidth="6"
          markerHeight="6"
          orient="auto-start-reverse"
        >
          <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#0284C7" />
        </marker>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="3" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
      </defs>

      {curves.map(({ rel, curve }, idx) => (
        <g key={idx} className="animate-fadeIn">
          <path
            d={curve.path}
            fill="none"
            stroke="#BAE0FD"
            strokeWidth="6"
            strokeOpacity="0.8"
            filter="url(#glow)"
          />
          <path
            d={curve.path}
            fill="none"
            stroke="#0284C7"
            strokeWidth="2.5"
            strokeDasharray="6 4"
            markerEnd="url(#rel-arrow)"
          />
          <circle cx={curve.start.x} cy={curve.start.y} r="4" fill="#0284C7" />
          <circle cx={curve.end.x} cy={curve.end.y} r="4" fill="#0284C7" />

          {rel.label && (
            <g transform={`translate(${curve.labelPosition.x}, ${curve.labelPosition.y})`}>
              <rect
                x="-50"
                y="-10"
                width="100"
                height="20"
                rx="10"
                fill="#0369A1"
                className="shadow-md"
              />
              <text
                x="0"
                y="4"
                textAnchor="middle"
                fontSize="10"
                fontWeight="bold"
                fill="#FFFFFF"
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
