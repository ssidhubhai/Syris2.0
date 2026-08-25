import { ExplanationDocument } from '@/types/explanation';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1';

export interface BackendSession {
  id: string;
  user_id?: string | null;
  title: string;
  subject: string;
  current_state: string;
  created_at: string;
  updated_at: string;
}

export interface BackendMessage {
  id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  attachments: any[];
  explanation_document_id?: string | null;
  created_at: string;
}

export interface BackendSessionDetail extends BackendSession {
  messages: BackendMessage[];
  problems: any[];
  latest_explanation?: {
    id: string;
    session_id: string;
    title: string;
    subject: string;
    intent: string;
    version: number;
    document_json: ExplanationDocument;
    validation_json: any;
    provider_metadata: any;
    created_at: string;
  } | null;
  latest_whiteboard?: any | null;
}

export interface ApiErrorResponse {
  error: {
    code: string;
    message: string;
    details?: any;
  };
  request_id?: string;
}

export interface GeminiSmokeResult {
  answer: string;
  confidence: 'high' | 'medium' | 'low';
}

export interface GeminiSmokeResponse {
  request_id: string;
  provider: string;
  model: string;
  latency_ms: number;
  token_usage?: {
    input_tokens: number;
    output_tokens: number;
    total_tokens: number;
    cached_tokens?: number | null;
  } | null;
  result: GeminiSmokeResult;
}

function generateRequestId(): string {
  return `req-fe-${Math.random().toString(36).substring(2, 11)}-${Date.now()}`;
}

async function request<T>(
  path: string,
  options: RequestInit = {},
  idempotencyKey?: string
): Promise<T> {
  const url = `${API_BASE}${path}`;
  const headers = new Headers(options.headers || {});

  if (!headers.has('Content-Type') && options.body) {
    headers.set('Content-Type', 'application/json');
  }

  headers.set('X-Request-ID', generateRequestId());

  if (idempotencyKey) {
    headers.set('X-Idempotency-Key', idempotencyKey);
  }

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      let errorData: ApiErrorResponse;
      try {
        errorData = await response.json();
      } catch {
        errorData = {
          error: {
            code: `HTTP_${response.status}`,
            message: `Request failed with status ${response.status}: ${response.statusText}`,
          },
        };
      }
      throw errorData;
    }

    return await response.json();
  } catch (err: any) {
    if (err.error) {
      throw err;
    }
    throw {
      error: {
        code: 'NETWORK_ERROR',
        message: err.message || 'Failed to connect to backend server.',
      },
    };
  }
}

export interface StudyAskResponse {
  request_id: string;
  session_id: string;
  explanation_document: ExplanationDocument;
}

export const syrisApi = {
  async checkHealth(): Promise<{ status: string; database: string }> {
    return request<{ status: string; database: string }>('/health');
  },

  async createSession(data: {
    id?: string;
    title?: string;
    subject?: string;
    initial_problem?: any;
  }, idempotencyKey?: string): Promise<BackendSession> {
    return request<BackendSession>(
      '/sessions',
      {
        method: 'POST',
        body: JSON.stringify(data),
      },
      idempotencyKey
    );
  },

  async getSession(sessionId: string): Promise<BackendSessionDetail> {
    return request<BackendSessionDetail>(`/sessions/${encodeURIComponent(sessionId)}`);
  },

  async listSessions(limit = 20, offset = 0): Promise<BackendSession[]> {
    return request<BackendSession[]>(`/sessions?limit=${limit}&offset=${offset}`);
  },

  async appendMessage(
    sessionId: string,
    message: { role: 'user' | 'assistant' | 'system'; content: string; attachments?: any[] },
    idempotencyKey?: string
  ): Promise<BackendMessage> {
    return request<BackendMessage>(
      `/sessions/${encodeURIComponent(sessionId)}/messages`,
      {
        method: 'POST',
        body: JSON.stringify(message),
      },
      idempotencyKey
    );
  },

  async saveExplanation(
    sessionId: string,
    document: ExplanationDocument,
    idempotencyKey?: string
  ): Promise<any> {
    return request<any>(
      `/sessions/${encodeURIComponent(sessionId)}/explanations`,
      {
        method: 'POST',
        body: JSON.stringify(document),
      },
      idempotencyKey
    );
  },

  async getLatestExplanation(sessionId: string): Promise<any> {
    return request<any>(`/sessions/${encodeURIComponent(sessionId)}/explanations/latest`);
  },

  async askStudyQuestion(payload: {
    session_id?: string | null;
    message: string;
    model_id?: string;
  }): Promise<StudyAskResponse> {
    return request<StudyAskResponse>('/study/ask', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  async runGeminiSmokeTest(payload?: {
    prompt?: string;
    model_id?: string;
  }): Promise<GeminiSmokeResponse> {
    return request<GeminiSmokeResponse>('/dev/gemini-smoke', {
      method: 'POST',
      body: JSON.stringify(payload || {}),
    });
  },
};


