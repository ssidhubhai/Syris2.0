import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { KaTeXMath } from '@/components/digital_paper/KaTeXMath';

describe('KaTeXMath Component', () => {
  it('should render mathematical formulas into HTML', () => {
    render(<KaTeXMath math="a_{\max} = g \tan\theta" displayMode={true} />);
    const mathWrapper = screen.getByTestId('katex-math');
    expect(mathWrapper).toBeInTheDocument();
    expect(mathWrapper.innerHTML).toContain('katex');
  });
});
