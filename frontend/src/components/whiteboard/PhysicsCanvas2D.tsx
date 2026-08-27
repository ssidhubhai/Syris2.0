import React, { useState } from 'react';
import { DiagramNodeContent } from '@/types/whiteboard';
import { KaTeXMath } from '../digital_paper/KaTeXMath';

interface PhysicsCanvas2DProps {
  content: DiagramNodeContent;
}

export const PhysicsCanvas2D: React.FC<PhysicsCanvas2DProps> = ({ content }) => {
  const [activeVectorId, setActiveVectorId] = useState<string | null>(null);

  const vectors = [
    {
      id: 'vec-mg',
      name: 'Gravity',
      latex: 'm g',
      color: '#DC2626',
      x1: 240,
      y1: 170,
      x2: 240,
      y2: 260,
      labelX: 250,
      labelY: 240,
    },
    {
      id: 'vec-pseudo',
      name: 'Pseudo Force',
      latex: 'm a_0',
      color: '#D97706',
      x1: 240,
      y1: 170,
      x2: 150,
      y2: 170,
      labelX: 160,
      labelY: 155,
    },
    {
      id: 'vec-normal',
      name: 'Normal Force',
      latex: 'N',
      color: '#2563EB',
      x1: 240,
      y1: 170,
      x2: 195,
      y2: 92,
      labelX: 175,
      labelY: 90,
    },
    {
      id: 'vec-friction',
      name: 'Friction',
      latex: 'f_s',
      color: '#059669',
      x1: 240,
      y1: 170,
      x2: 162,
      y2: 215,
      labelX: 140,
      labelY: 235,
    },
  ];

  return (
    <div className="bg-paper-50/80 rounded-lg border border-[#E5E3D8] p-3" data-testid="physics-canvas-2d">
      <div className="text-xs font-mono font-bold text-ink-700 uppercase tracking-wide mb-1 pb-1 border-b border-[#E5E3D8]/60">
        {content.title || 'Free Body Diagram'}
      </div>

      <div className="relative flex justify-center items-center py-2">
        <svg
          viewBox="0 0 400 300"
          className="w-full h-auto max-w-[380px] select-none"
          role="img"
          aria-label="Free body diagram of block on accelerating wedge"
        >
          <defs>
            {vectors.map((vec) => (
              <marker
                key={vec.id}
                id={`arrow-${vec.id}`}
                viewBox="0 0 10 10"
                refX="8"
                refY="5"
                markerWidth="6"
                markerHeight="6"
                orient="auto-start-reverse"
              >
                <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill={vec.color} />
              </marker>
            ))}
            <pattern id="ground-hatch" width="8" height="8" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
              <line x1="0" y1="0" x2="0" y2="8" stroke="#D1D5DB" strokeWidth="1.5" />
            </pattern>
          </defs>

          <g stroke="#E5E7EB" strokeWidth="1" strokeDasharray="3 3">
            <line x1="20" y1="270" x2="380" y2="270" />
            <line x1="50" y1="20" x2="50" y2="280" />
          </g>

          <line x1="30" y1="270" x2="370" y2="270" stroke="#4B5563" strokeWidth="2" />
          <rect x="30" y="270" width="340" height="12" fill="url(#ground-hatch)" />

          <polygon
            points="50,270 350,270 350,96.8"
            fill="#E2E8F0"
            stroke="#475569"
            strokeWidth="1.5"
          />

          <path
            d="M 100 270 A 50 50 0 0 0 93.3 245"
            fill="none"
            stroke="#0284C7"
            strokeWidth="1.5"
          />
          <text x="110" y="260" fontSize="13" fontWeight="bold" fill="#0284C7" fontFamily="Georgia, serif">
            θ
          </text>

          <g transform="translate(310, 245)">
            <line x1="0" y1="0" x2="35" y2="0" stroke="#D97706" strokeWidth="1.5" markerEnd="url(#arrow-vec-pseudo)" />
            <text x="5" y="-5" fontSize="11" fontWeight="bold" fill="#D97706">
              a_0 →
            </text>
          </g>

          <g transform="translate(240, 170) rotate(30)">
            <rect
              x="-35"
              y="-25"
              width="70"
              height="50"
              rx="2"
              fill="#FEF3C7"
              stroke="#B45309"
              strokeWidth="1.5"
            />
            <circle cx="0" cy="0" r="3" fill="#B45309" />
            <text x="-12" y="5" fontSize="12" fontWeight="bold" fill="#78350F">
              m
            </text>
          </g>

          <g stroke="#94A3B8" strokeWidth="1" strokeDasharray="2 2">
            <line x1="240" y1="170" x2="180" y2="66" />
            <line x1="240" y1="170" x2="136" y2="230" />
          </g>

          {vectors.map((vec) => {
            const isHovered = activeVectorId === vec.id;
            return (
              <g
                key={vec.id}
                onMouseEnter={() => setActiveVectorId(vec.id)}
                onMouseLeave={() => setActiveVectorId(null)}
                className="cursor-pointer transition-opacity"
                opacity={activeVectorId && !isHovered ? 0.35 : 1}
              >
                <line
                  x1={vec.x1}
                  y1={vec.y1}
                  x2={vec.x2}
                  y2={vec.y2}
                  stroke="transparent"
                  strokeWidth="16"
                />
                <line
                  x1={vec.x1}
                  y1={vec.y1}
                  x2={vec.x2}
                  y2={vec.y2}
                  stroke={vec.color}
                  strokeWidth={isHovered ? 3 : 2}
                  markerEnd={`url(#arrow-${vec.id})`}
                />
                <text
                  x={vec.labelX}
                  y={vec.labelY}
                  fontSize={isHovered ? '13' : '11'}
                  fontWeight="bold"
                  fill={vec.color}
                  fontFamily="Georgia, serif"
                >
                  {vec.latex}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      <div className="flex flex-wrap items-center justify-center gap-1.5 pt-2 border-t border-paper-200 text-xs">
        {vectors.map((vec) => (
          <button
            key={vec.id}
            type="button"
            onMouseEnter={() => setActiveVectorId(vec.id)}
            onMouseLeave={() => setActiveVectorId(null)}
            className={`px-2 py-0.5 rounded text-[11px] font-mono border flex items-center gap-1 transition-all ${
              activeVectorId === vec.id
                ? 'bg-white border-academic-physics-accent text-ink-900 shadow-xs'
                : 'bg-white/50 border-paper-200 text-ink-600 hover:bg-white'
            }`}
          >
            <span className="w-2 h-2 rounded-full" style={{ backgroundColor: vec.color }} />
            <span>{vec.name}</span>
            <KaTeXMath math={vec.latex} displayMode={false} className="text-[10px]" />
          </button>
        ))}
      </div>
    </div>
  );
};
