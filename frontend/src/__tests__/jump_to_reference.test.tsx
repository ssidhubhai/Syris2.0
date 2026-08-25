import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { InlineMarkdown } from '@/components/digital_paper/InlineMarkdown';
import { StickyContextBar } from '@/components/digital_paper/StickyContextBar';
import { canonicalPhysicsFixture } from '@/fixtures/canonical_physics_fixture';

describe('Interactive Navigation & Jump-to-Reference', () => {
  it('should render reference links and trigger jump on click', () => {
    const handleJump = vi.fn();
    render(
      <InlineMarkdown
        content="Check [Eq. (1)](ref://node-eq-normal) for normal force."
        onJump={handleJump}
      />
    );

    const refButton = screen.getByText(/Eq\. \(1\)/i);
    expect(refButton).toBeInTheDocument();

    fireEvent.click(refButton);
    expect(handleJump).toHaveBeenCalledWith('node-eq-normal');
  });

  it('should render StickyContextBar when visible and trigger jump', () => {
    const handleJump = vi.fn();
    const stickyNodes = canonicalPhysicsFixture.nodes.filter(
      (n) => n.layout_preference === 'sticky_context'
    );

    render(
      <StickyContextBar
        stickyNodes={stickyNodes}
        onJump={handleJump}
        visible={true}
      />
    );

    expect(screen.getByTestId('sticky-context-bar')).toBeInTheDocument();
    expect(screen.getByText(/Active Governing Law:/i)).toBeInTheDocument();

    const jumpButton = screen.getByText(/View In Law Card/i);
    fireEvent.click(jumpButton);
    expect(handleJump).toHaveBeenCalledWith('node-sticky-law');
  });
});
