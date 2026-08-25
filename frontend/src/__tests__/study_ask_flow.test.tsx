import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { DigitalPaperWorkspace } from '@/components/digital_paper/DigitalPaperWorkspace';
import { syrisApi, StudyAskResponse } from '@/services/apiClient';

describe('Phase 4A — Real AI Explanation Pipeline Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('submits student question to backend /study/ask and renders generated explanation document', async () => {
    const mockGeneratedDoc = {
      document_id: 'doc-ai-friction-401',
      session_id: 'sess-ai-friction-401',
      title: 'Microscopic Origin of Contact Friction',
      intent: 'concept_explanation',
      subject: 'physics' as const,
      language: 'english',
      nodes: [
        {
          id: 'node-head-ai-1',
          type: 'heading' as const,
          content: { text: 'Why Contact Friction Opposes Relative Motion', level: 1 },
          importance: 'critical' as const,
        },
        {
          id: 'node-text-ai-1',
          type: 'text' as const,
          content: {
            markdown: 'Friction originates from microscopic roughness and intermolecular electrostatic adhesion between contacting surfaces.',
          },
          importance: 'supporting' as const,
        },
        {
          id: 'node-def-ai-1',
          type: 'definition' as const,
          content: {
            title: "Coulomb's Friction Law",
            latex: 'f_k = \\mu_k N',
            annotation: 'Opposes the direction of relative surface velocity.',
          },
          importance: 'critical' as const,
        },
      ],
      relationships: [
        {
          from: 'node-head-ai-1',
          to: 'node-text-ai-1',
          type: 'explains' as const,
        },
      ],
      validation: {
        math_verified: false,
        domain_verified: false,
        verifier_used: 'semantic_validator_phase4a',
        flagged_issues: [],
      },
      source_metadata: {
        provider: 'google',
        model: 'gemini-3.5-flash-lite',
        generation_time_ms: 620,
      },
    };

    const mockResponse: StudyAskResponse = {
      request_id: 'req-ask-test-101',
      session_id: 'sess-ai-friction-401',
      explanation_document: mockGeneratedDoc,
    };

    const askSpy = vi.spyOn(syrisApi, 'askStudyQuestion').mockResolvedValue(mockResponse);

    render(<DigitalPaperWorkspace />);

    // Type in user query
    const input = screen.getByLabelText(/Ask a JEE question/i);
    fireEvent.change(input, {
      target: { value: 'Why does friction oppose relative motion?' },
    });

    // Click submit
    const sendBtn = screen.getByLabelText(/Send Query/i);
    fireEvent.click(sendBtn);

    // Verify loading indicator is displayed
    expect(askSpy).toHaveBeenCalledWith({
      session_id: null,
      message: 'Why does friction oppose relative motion?',
    });

    // Wait for the digital paper to re-render with the AI generated document
    await waitFor(() => {
      expect(
        screen.getByText('Why Contact Friction Opposes Relative Motion')
      ).toBeDefined();
    });

    expect(
      screen.getByText(/intermolecular electrostatic adhesion/i)
    ).toBeDefined();
    expect(screen.getByText("Coulomb's Friction Law")).toBeDefined();
  });

  it('displays friendly error notice when AI backend returns an error', async () => {
    vi.spyOn(syrisApi, 'askStudyQuestion').mockRejectedValue({
      error: {
        code: 'RATE_LIMIT_EXCEEDED',
        message: 'Google Gemini quota limit reached. Please wait a moment before trying again.',
      },
      request_id: 'err-rate-limit',
    });

    render(<DigitalPaperWorkspace />);

    const input = screen.getByLabelText(/Ask a JEE question/i);
    fireEvent.change(input, {
      target: { value: 'Why does friction act on the wedge?' },
    });

    const sendBtn = screen.getByLabelText(/Send Query/i);
    fireEvent.click(sendBtn);

    await waitFor(() => {
      expect(
        screen.getByText(/Google Gemini quota limit reached/i)
      ).toBeDefined();
    });
  });
});
