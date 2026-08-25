import React from 'react';
import { KaTeXMath } from './KaTeXMath';

interface InlineMarkdownProps {
  content: string;
  onJump?: (nodeId: string) => void;
  className?: string;
}

export const InlineMarkdown: React.FC<InlineMarkdownProps> = ({
  content,
  onJump,
  className = '',
}) => {
  const tokens = parseMarkdownTokens(content);

  return (
    <span className={`inline-markdown leading-relaxed text-ink-800 ${className}`}>
      {tokens.map((token, index) => {
        if (token.type === 'math') {
          return <KaTeXMath key={index} math={token.value} displayMode={false} />;
        }
        if (token.type === 'ref') {
          return (
            <button
              key={index}
              type="button"
              onClick={() => onJump?.(token.refId || '')}
              className="inline-flex items-center mx-1 px-1.5 py-0.5 rounded text-xs font-semibold bg-academic-physics-bg text-academic-physics-ink border border-academic-physics-border hover:bg-academic-physics-border/40 transition-colors focus:outline-none focus:ring-2 focus:ring-academic-physics-accent"
              title={`Jump to ${token.label}`}
              data-ref-id={token.refId}
            >
              ↗ {token.label}
            </button>
          );
        }
        if (token.type === 'bold') {
          return (
            <strong key={index} className="font-semibold text-ink-900">
              {token.value}
            </strong>
          );
        }
        return <span key={index}>{token.value}</span>;
      })}
    </span>
  );
};

interface Token {
  type: 'text' | 'math' | 'ref' | 'bold';
  value: string;
  refId?: string;
  label?: string;
}

function parseMarkdownTokens(input: string): Token[] {
  const tokens: Token[] = [];
  let remaining = input;

  while (remaining.length > 0) {
    const refMatch = remaining.match(/^\[([^\]]+)\]\(ref:\/\/([^\)]+)\)/);
    if (refMatch) {
      tokens.push({
        type: 'ref',
        value: refMatch[0],
        label: refMatch[1],
        refId: refMatch[2],
      });
      remaining = remaining.slice(refMatch[0].length);
      continue;
    }

    const mathMatch = remaining.match(/^\$([^\$]+)\$/);
    if (mathMatch) {
      tokens.push({
        type: 'math',
        value: mathMatch[1],
      });
      remaining = remaining.slice(mathMatch[0].length);
      continue;
    }

    const boldMatch = remaining.match(/^\*\*([^\*]+)\*\*/);
    if (boldMatch) {
      tokens.push({
        type: 'bold',
        value: boldMatch[1],
      });
      remaining = remaining.slice(boldMatch[0].length);
      continue;
    }

    const nextSpecial = remaining.search(/(\[|\$|\*\*)/);
    if (nextSpecial === -1) {
      tokens.push({ type: 'text', value: remaining });
      break;
    } else if (nextSpecial === 0) {
      tokens.push({ type: 'text', value: remaining[0] });
      remaining = remaining.slice(1);
    } else {
      tokens.push({ type: 'text', value: remaining.slice(0, nextSpecial) });
      remaining = remaining.slice(nextSpecial);
    }
  }

  return tokens;
}
