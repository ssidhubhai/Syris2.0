import React, { useState } from 'react';
import { syrisApi, GeminiSmokeResponse, ApiErrorResponse } from '@/services/apiClient';
import { Sparkles, Play, RefreshCw, AlertCircle, CheckCircle2, Cpu, ShieldCheck } from 'lucide-react';

const DEFAULT_PROMPT = `You are being tested as an educational AI system.
Return a very short answer to:
Why does friction oppose the tendency of relative motion?

Return only the requested structured fields.`;

export const DevSmokeTestPanel: React.FC = () => {
  const [prompt, setPrompt] = useState(DEFAULT_PROMPT);
  const [modelId, setModelId] = useState('gemini-3.5-flash-lite');
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<GeminiSmokeResponse | null>(null);
  const [error, setError] = useState<ApiErrorResponse['error'] | null>(null);
  const [errorRequestId, setErrorRequestId] = useState<string | null>(null);

  const handleRunSmokeTest = async () => {
    setIsLoading(true);
    setError(null);
    setErrorRequestId(null);
    setResponse(null);

    try {
      const data = await syrisApi.runGeminiSmokeTest({
        prompt: prompt.trim(),
        model_id: modelId,
      });
      setResponse(data);
    } catch (err: any) {
      if (err.error) {
        setError(err.error);
        setErrorRequestId(err.request_id || null);
      } else {
        setError({
          code: 'CLIENT_ERROR',
          message: err.message || 'An unexpected client error occurred.',
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetPrompt = () => {
    setPrompt(DEFAULT_PROMPT);
  };

  return (
    <div className="flex flex-col gap-4 p-4 bg-ink-900 text-paper-100 font-mono text-xs rounded-lg" data-testid="dev-smoke-test-panel">
      {/* Header Banner */}
      <div className="flex items-center justify-between border-b border-ink-700 pb-3">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-academic-physics-accent" />
          <h4 className="text-sm font-bold text-white tracking-wide">
            Development Gemini Smoke Test
          </h4>
        </div>
        <div className="flex items-center gap-1.5 px-2 py-0.5 rounded bg-emerald-950/80 border border-emerald-500/40 text-[10px] text-emerald-300">
          <ShieldCheck className="w-3 h-3 text-emerald-400" />
          <span>PHASE 3C ISOLATED ENDPOINT</span>
        </div>
      </div>

      {/* Model Selection */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-1.5 text-ink-400 text-[11px]">
          <Cpu className="w-3.5 h-3.5 text-academic-physics-accent" />
          <span>Certified Candidate:</span>
        </div>
        <select
          value={modelId}
          onChange={(e) => setModelId(e.target.value)}
          disabled={isLoading}
          className="bg-ink-800 border border-ink-600 rounded px-2.5 py-1 text-white text-xs font-mono focus:outline-none focus:border-academic-physics-accent"
        >
          <option value="gemini-3.5-flash-lite">gemini-3.5-flash-lite (CERTIFIED_FOR_DEV)</option>
          <option value="gemini-3.5-flash">gemini-3.5-flash (CERTIFIED_FOR_DEV)</option>
          <option value="gemini-2.5-flash">gemini-2.5-flash (CERTIFIED_FOR_DEV)</option>
        </select>
      </div>

      {/* Prompt Input */}
      <div className="flex flex-col gap-1.5">
        <div className="flex items-center justify-between">
          <label htmlFor="smoke-prompt-input" className="text-[11px] text-ink-400">
            Deterministic Test Prompt:
          </label>
          <button
            type="button"
            onClick={handleResetPrompt}
            disabled={isLoading}
            className="text-[10px] text-ink-400 hover:text-white underline cursor-pointer"
          >
            Reset Default Prompt
          </button>
        </div>
        <textarea
          id="smoke-prompt-input"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          disabled={isLoading}
          rows={5}
          className="w-full bg-ink-950 border border-ink-700 rounded p-2.5 text-paper-100 text-xs font-mono focus:outline-none focus:border-academic-physics-accent leading-relaxed resize-none selection:bg-academic-physics-accent/30"
          placeholder="Enter prompt for structured test..."
        />
      </div>

      {/* Run Action Button */}
      <div className="flex justify-end">
        <button
          type="button"
          onClick={handleRunSmokeTest}
          disabled={isLoading || !prompt.trim()}
          className={`px-4 py-2 rounded text-xs font-bold font-mono flex items-center gap-2 transition-all ${
            isLoading || !prompt.trim()
              ? 'bg-ink-700 text-ink-500 cursor-not-allowed'
              : 'bg-academic-physics-accent hover:bg-academic-physics-accent/90 text-white shadow-lg hover:shadow-academic-physics-accent/20 cursor-pointer'
          }`}
          data-testid="run-smoke-test-btn"
        >
          {isLoading ? (
            <>
              <RefreshCw className="w-3.5 h-3.5 animate-spin" />
              <span>Calling Gemini (FastAPI &rarr; GoogleProvider)...</span>
            </>
          ) : (
            <>
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>Run Gemini Smoke Test</span>
            </>
          )}
        </button>
      </div>

      {/* Structured Result Display */}
      {response && (
        <div className="mt-2 p-3 bg-ink-950 border border-emerald-600/40 rounded-lg flex flex-col gap-3 animate-fadeIn" data-testid="smoke-test-result">
          <div className="flex items-center justify-between border-b border-ink-800 pb-2">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span className="font-bold text-emerald-300 text-xs">
                Structured Result Validated
              </span>
            </div>
            <div className="flex items-center gap-2 text-[10px] text-ink-400">
              <span className="px-1.5 py-0.5 rounded bg-ink-800 text-ink-300">
                {response.latency_ms} ms
              </span>
              {response.token_usage && (
                <span className="px-1.5 py-0.5 rounded bg-ink-800 text-ink-300">
                  {response.token_usage.total_tokens} tokens
                </span>
              )}
            </div>
          </div>

          {/* Telemetry Metadata Grid */}
          <div className="grid grid-cols-2 gap-2 text-[11px] bg-ink-900/80 p-2 rounded border border-ink-800">
            <div>
              <span className="text-ink-400">Provider:</span>{' '}
              <span className="text-paper-100 font-bold">{response.provider}</span>
            </div>
            <div>
              <span className="text-ink-400">Model:</span>{' '}
              <span className="text-academic-physics-border">{response.model}</span>
            </div>
            <div className="col-span-2 truncate">
              <span className="text-ink-400">Request ID:</span>{' '}
              <span className="text-ink-300 font-mono text-[10px]">{response.request_id}</span>
            </div>
          </div>

          {/* Structured Fields Output */}
          <div className="flex flex-col gap-2">
            <div className="flex items-center justify-between">
              <span className="text-[11px] text-ink-400 uppercase tracking-wider">Answer:</span>
              <span
                className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                  response.result.confidence === 'high'
                    ? 'bg-emerald-950 text-emerald-400 border border-emerald-600/40'
                    : response.result.confidence === 'medium'
                    ? 'bg-amber-950 text-amber-400 border border-amber-600/40'
                    : 'bg-rose-950 text-rose-400 border border-rose-600/40'
                }`}
              >
                Confidence: {response.result.confidence.toUpperCase()}
              </span>
            </div>
            <div className="p-2.5 bg-ink-900 rounded border border-ink-700 text-emerald-200 text-xs leading-relaxed">
              {response.result.answer}
            </div>
          </div>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="mt-2 p-3 bg-rose-950/50 border border-rose-600/50 rounded-lg flex flex-col gap-2 text-rose-200" data-testid="smoke-test-error">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
            <span className="font-bold text-xs">Error: {error.code}</span>
          </div>
          <p className="text-xs leading-relaxed text-rose-300 font-sans">
            {error.message}
          </p>
          {errorRequestId && (
            <div className="text-[10px] text-rose-400/80">
              Request ID: <span className="font-mono">{errorRequestId}</span>
            </div>
          )}
          {error.details && (
            <pre className="text-[10px] bg-ink-950 p-2 rounded overflow-x-auto text-rose-400">
              {JSON.stringify(error.details, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  );
};
