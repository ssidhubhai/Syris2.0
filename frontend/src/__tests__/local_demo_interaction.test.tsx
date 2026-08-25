import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { DigitalPaperWorkspace } from '@/components/digital_paper/DigitalPaperWorkspace';
import { matchDemoFixture, DEV_FIXTURES } from '@/fixtures';
import { syrisApi } from '@/services/apiClient';

describe('Phase 1B & 4A — Study Workspace Interaction Flow', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('correctly matches keyword queries to fixtures in deterministic helper', () => {
    expect(matchDemoFixture('why is friction acting downward on the wedge?')?.key).toBe(
      'canonical_physics'
    );
    expect(matchDemoFixture('why is electric potential a scalar quantity?')?.key).toBe(
      'concept_physics'
    );
    expect(matchDemoFixture('how to decide between sn1 and sn2 mechanisms?')?.key).toBe(
      'chemistry_comparison'
    );
    expect(matchDemoFixture('what is centripetal acceleration and how to derive it?')?.key).toBe(
      'compact_definition'
    );
    expect(matchDemoFixture("evaluate definite integral using feynman's trick")?.key).toBe(
      'canonical_math'
    );
    expect(matchDemoFixture('some completely random unrelated string')).toBeNull();
  });

  it('updates the active digital paper when submitting a recognized question', async () => {
    vi.spyOn(syrisApi, 'askStudyQuestion').mockResolvedValue({
      request_id: 'req-chem-001',
      session_id: 'sess-chem-001',
      explanation_document: DEV_FIXTURES.chemistry_comparison.doc,
    });

    render(<DigitalPaperWorkspace />);

    // Starts on Physics
    expect(screen.getByText('physics')).toBeInTheDocument();

    // Type chemistry query in UnifiedInputBar
    const input = screen.getByRole('textbox', { name: /ask a jee question/i });
    fireEvent.change(input, { target: { value: 'sn1 vs sn2 substitution' } });

    const sendBtn = screen.getByRole('button', { name: /send query/i });
    fireEvent.click(sendBtn);

    // Document switches to Chemistry
    await waitFor(() => {
      expect(screen.getByText('chemistry')).toBeInTheDocument();
    });
  });

  it('shows error notice when backend ask call fails', async () => {
    vi.spyOn(syrisApi, 'askStudyQuestion').mockRejectedValue({
      error: {
        code: 'NETWORK_ERROR',
        message: 'Could not connect to AI study companion.',
      },
    });

    render(<DigitalPaperWorkspace />);

    const input = screen.getByRole('textbox', { name: /ask a jee question/i });
    fireEvent.change(input, { target: { value: 'write me a poem about trees' } });

    const sendBtn = screen.getByRole('button', { name: /send query/i });
    fireEvent.click(sendBtn);

    // Banner message should be displayed
    await waitFor(() => {
      expect(
        screen.getByText(/Could not connect to AI study companion/i)
      ).toBeInTheDocument();
    });

    // Clicking a suggestion chip from the banner loads that study sheet
    vi.spyOn(syrisApi, 'askStudyQuestion').mockResolvedValue({
      request_id: 'req-math-001',
      session_id: 'sess-math-001',
      explanation_document: DEV_FIXTURES.canonical_math.doc,
    });

    const mathChip = screen.getByRole('button', { name: /Feynman's Integral Trick →/i });
    fireEvent.click(mathChip);

    await waitFor(() => {
      expect(screen.getByText('mathematics')).toBeInTheDocument();
    });
  });

  it('loads study sheet when clicking quick topic chips', async () => {
    vi.spyOn(syrisApi, 'askStudyQuestion').mockResolvedValue({
      request_id: 'req-scalar-001',
      session_id: 'sess-scalar-001',
      explanation_document: DEV_FIXTURES.concept_physics.doc,
    });

    render(<DigitalPaperWorkspace />);

    const chip = screen.getByRole('button', { name: /Scalar Potential/i });
    fireEvent.click(chip);

    await waitFor(() => {
      expect(screen.getByText(/Why Electric Potential is a Scalar Quantity/i)).toBeInTheDocument();
    });
  });
});

