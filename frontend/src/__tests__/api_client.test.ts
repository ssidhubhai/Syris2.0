import { describe, it, expect, vi, beforeEach } from 'vitest';
import { syrisApi } from '@/services/apiClient';
import { canonicalPhysicsFixture } from '@/fixtures/canonical_physics_fixture';

describe('Frontend API Client (Phase 2 Session Integration)', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('creates a study session with generated request ID and optional idempotency key', async () => {
    const mockSessionResponse = {
      id: 'sess-fe-test-123',
      title: 'Kinematics Session',
      subject: 'physics',
      current_state: 'active',
      created_at: '2026-08-24T22:00:00Z',
      updated_at: '2026-08-24T22:00:00Z',
    };

    const fetchSpy = vi.spyOn(global, 'fetch').mockResolvedValueOnce({
      ok: true,
      json: async () => mockSessionResponse,
    } as Response);

    const session = await syrisApi.createSession(
      { title: 'Kinematics Session', subject: 'physics' },
      'idem-fe-001'
    );

    expect(session.id).toBe('sess-fe-test-123');
    expect(fetchSpy).toHaveBeenCalledTimes(1);

    const [calledUrl, calledOptions] = fetchSpy.mock.calls[0];
    expect(calledUrl).toContain('/sessions');
    expect(calledOptions?.method).toBe('POST');
    
    const headers = calledOptions?.headers as Headers;
    expect(headers.get('X-Idempotency-Key')).toBe('idem-fe-001');
    expect(headers.get('X-Request-ID')).toMatch(/^req-fe-/);
  });

  it('persists a canonical explanation document to a session', async () => {
    const mockDocResponse = {
      id: canonicalPhysicsFixture.document_id,
      session_id: 'sess-fe-test-123',
      title: canonicalPhysicsFixture.title,
      subject: canonicalPhysicsFixture.subject,
      intent: canonicalPhysicsFixture.intent,
      version: 1,
      document_json: canonicalPhysicsFixture,
      validation_json: {},
      provider_metadata: {},
      created_at: '2026-08-24T22:00:00Z',
    };

    const fetchSpy = vi.spyOn(global, 'fetch').mockResolvedValueOnce({
      ok: true,
      json: async () => mockDocResponse,
    } as Response);

    const result = await syrisApi.saveExplanation('sess-fe-test-123', canonicalPhysicsFixture);
    expect(result.id).toBe(canonicalPhysicsFixture.document_id);
    expect(fetchSpy).toHaveBeenCalledTimes(1);
    expect(fetchSpy.mock.calls[0][0]).toContain('/sessions/sess-fe-test-123/explanations');
  });

  it('handles standard backend error envelopes gracefully', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValueOnce({
      ok: false,
      status: 404,
      statusText: 'Not Found',
      json: async () => ({
        error: {
          code: 'SESSION_NOT_FOUND',
          message: "Session 'sess-invalid' was not found.",
        },
        request_id: 'req-err-123',
      }),
    } as Response);

    await expect(syrisApi.getSession('sess-invalid')).rejects.toEqual({
      error: {
        code: 'SESSION_NOT_FOUND',
        message: "Session 'sess-invalid' was not found.",
      },
      request_id: 'req-err-123',
    });
  });
});
