import React, { useMemo } from 'react';
import katex from 'katex';

interface KaTeXMathProps {
  math: string;
  displayMode?: boolean;
  className?: string;
}

export const KaTeXMath: React.FC<KaTeXMathProps> = ({
  math,
  displayMode = false,
  className = '',
}) => {
  const renderedHtml = useMemo(() => {
    try {
      const trimmed = (math || '').trim();
      if (!trimmed) return '';
      
      // If string is plain english text with spaces and no math operators, wrap in \text{}
      const formatted =
        !/[\_\^\\\{\}\$\=\+\-\*\/\<\>]/.test(trimmed) && trimmed.includes(' ')
          ? `\\text{${trimmed}}`
          : trimmed;

      return katex.renderToString(formatted, {
        displayMode,
        throwOnError: false,
        strict: false,
      });
    } catch {
      return math;
    }
  }, [math, displayMode]);

  return (
    <span
      className={`katex-math-wrapper ${className}`}
      data-testid="katex-math"
      dangerouslySetInnerHTML={{ __html: renderedHtml }}
    />
  );
};
