import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { DevSmokeTestPanel } from '@/components/dev/DevSmokeTestPanel';
import { syrisApi } from '@/services/apiClient';

describe('Phase 3C — DevSmokeTestPanel Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders development banner, model selector, prompt textarea and run button', () => {
    render(<DevSmokeTestPanel />);

    expect(screen.getByText('Development Gemini Smoke Test')).toBeDefined();
    expect(screen.getByText('PHASE 3C ISOLATED ENDPOINT')).toBeDefined();
    expect(screen.getByRole('combobox')).toBeDefined();
    expect(screen.getByLabelText(/Deterministic Test Prompt:/i)).toBeDefined();
    expect(screen.getByTestId('run-smoke-test-btn')).toBeDefined();
  });

  it('executes smoke test and displays validated structured response and telemetry', async () => {
    const mockSmokeResponse = {
      request_id: 'smoke-fe-test-123',
      provider: 'google',
      model: 'gemini-3.5-flash-lite',
      latency_ms: 320,
      token_usage: {
        input_tokens: 28,
        output_tokens: 15,
        total_tokens: 43,
        cached_tokens: null,
      },
      result: {
        answer: 'Friction opposes relative motion due to microscopic surface asperities interlocking and intermolecular electrostatic attraction.',
        confidence: 'high' as const,
      },
    };

    vi.spyOn(syrisApi, 'runGeminiSmokeTest').mockResolvedValue(mockSmokeResponse);

    render(<DevSmokeTestPanel />);

    const runBtn = screen.getByTestId('run-smoke-test-btn');
    fireEvent.click(runBtn);

    await waitFor(() => {
      expect(screen.getByTestId('smoke-test-result')).toBeDefined();
    });

    expect(screen.getByText('Structured Result Validated')).toBeDefined();
    expect(screen.getByText('320 ms')).toBeDefined();
    expect(screen.getByText('43 tokens')).toBeDefined();
    expect(screen.getByText('smoke-fe-test-123')).toBeDefined();
    expect(screen.getByText(/Confidence:\s*HIGH/i)).toBeDefined();
    expect(
      screen.getByText(/microscopic surface asperities interlocking/i)
    ).toBeDefined();
  });

  it('displays normalized error banner when backend returns error envelope', async () => {
    const mockError = {
      error: {
        code: 'RATE_LIMIT_EXCEEDED',
        message: 'Google Gemini quota limit exceeded (429): Resource exhausted.',
        details: { status_code: 429 },
      },
      request_id: 'err-req-999',
    };

    vi.spyOn(syrisApi, 'runGeminiSmokeTest').mockRejectedValue(mockError);

    render(<DevSmokeTestPanel />);

    const runBtn = screen.getByTestId('run-smoke-test-btn');
    fireEvent.click(runBtn);

    await waitFor(() => {
      expect(screen.getByTestId('smoke-test-error')).toBeDefined();
    });

    expect(screen.getByText(/Error: RATE_LIMIT_EXCEEDED/i)).toBeDefined();
    expect(screen.getByText(/Google Gemini quota limit exceeded/i)).toBeDefined();
    expect(screen.getByText('err-req-999')).toBeDefined();
  });
});
