import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { DigitalPaperWorkspace } from '@/components/digital_paper/DigitalPaperWorkspace';
import { WorkspaceHeader } from '@/components/shell/WorkspaceHeader';
import { WorkspaceSidebar } from '@/components/shell/WorkspaceSidebar';
import { HistoryDrawer } from '@/components/shell/HistoryDrawer';
import { DEV_FIXTURES } from '@/fixtures';

describe('Phase 1B — Workspace Application Shell', () => {
  it('renders header with branding, subject badge, and document title', () => {
    const doc = DEV_FIXTURES.canonical_physics.doc;
    render(
      <WorkspaceHeader
        document={doc}
        zoomScale={1}
        zoomIn={vi.fn()}
        zoomOut={vi.fn()}
        resetZoom={vi.fn()}
        focusedNodeId={null}
        onClearFocus={vi.fn()}
        onToggleHistory={vi.fn()}
        isHistoryOpen={false}
        onToggleSidebar={vi.fn()}
        onOpenInspector={vi.fn()}
      />
    );

    expect(screen.getByText('SYRIS')).toBeInTheDocument();
    expect(screen.getByText('physics')).toBeInTheDocument();
    expect(screen.getByText(doc.title)).toBeInTheDocument();
  });

  it('renders sidebar with minimal navigation and V2 badges', () => {
    const onSelect = vi.fn();
    render(
      <WorkspaceSidebar
        currentSection="home"
        onSelectSection={onSelect}
        isOpenMobile={false}
        onCloseMobile={vi.fn()}
        isCollapsedDesktop={false}
        onToggleCollapseDesktop={vi.fn()}
      />
    );

    expect(screen.getByText('Study Sheet')).toBeInTheDocument();
    expect(screen.getByText('History')).toBeInTheDocument();
    expect(screen.getByText('Practice')).toBeInTheDocument();
    expect(screen.getByText('Concepts')).toBeInTheDocument();
    expect(screen.getByText('Mistakes')).toBeInTheDocument();

    const v2Badges = screen.getAllByText('V2');
    expect(v2Badges.length).toBeGreaterThanOrEqual(3);
  });

  it('opens history drawer and lists demo study sessions', () => {
    render(<DigitalPaperWorkspace />);

    // Toggle history drawer
    const historyBtn = screen.getByRole('button', { name: /toggle history/i });
    fireEvent.click(historyBtn);

    expect(screen.getByRole('dialog', { name: /study session history/i })).toBeInTheDocument();
    expect(screen.getByText('STUDY SESSIONS')).toBeInTheDocument();
    expect(screen.getByText(/Wedge Incline with Static Friction/i)).toBeInTheDocument();
  });

  it('restores a different session when clicked in history drawer', () => {
    render(<DigitalPaperWorkspace />);

    // Open History
    const historyBtn = screen.getByRole('button', { name: /toggle history/i });
    fireEvent.click(historyBtn);

    // Click on Chemistry SN1 vs SN2 session
    const chemSession = screen.getByText(/Bimolecular \(SN2\) vs Unimolecular \(SN1\)/i);
    fireEvent.click(chemSession);

    // Header and document should update to Chemistry
    expect(screen.getByText('chemistry')).toBeInTheDocument();
  });
});
