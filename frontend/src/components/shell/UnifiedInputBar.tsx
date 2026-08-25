import React, { useState, useRef } from 'react';
import { Send, Image as ImageIcon, FileEdit, Mic, Sparkles, X, Info, HelpCircle, RefreshCw } from 'lucide-react';
import { DemoNotice } from '@/hooks/useStudyWorkspaceSession';

interface UnifiedInputBarProps {
  currentQuery: string;
  onSubmitQuery: (query: string) => void;
  demoNotice: DemoNotice | null;
  onClearDemoNotice: () => void;
  isTransitioning?: boolean;
  isGenerating?: boolean;
}


export const UnifiedInputBar: React.FC<UnifiedInputBarProps> = ({
  currentQuery,
  onSubmitQuery,
  demoNotice,
  onClearDemoNotice,
  isTransitioning = false,
  isGenerating = false,
}) => {
  const [inputValue, setInputValue] = useState<string>('');
  const [activeTooltip, setActiveTooltip] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const sampleChips = [
    { label: 'Wedge Friction', query: 'Why is friction acting downward on the wedge?' },
    { label: 'Scalar Potential', query: 'Why is electric potential a scalar quantity?' },
    { label: 'SN1 vs SN2', query: 'How to decide between SN1 and SN2 mechanisms?' },
    { label: 'Centripetal Accel', query: 'What is centripetal acceleration?' },
    { label: "Feynman's Integral", query: "Evaluate definite integral using Feynman's trick" },
  ];

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    const queryToSubmit = inputValue.trim();
    if (queryToSubmit && !isGenerating) {
      onSubmitQuery(queryToSubmit);
      setInputValue('');
    }
  };

  const handleChipClick = (query: string) => {
    if (!isGenerating) {
      onSubmitQuery(query);
      setInputValue('');
    }
  };

  return (
    <div className="fixed bottom-0 left-0 right-0 z-30 pointer-events-none p-3 sm:p-4 flex flex-col items-center">
      {/* Demo Guidance Notice Banner */}
      {demoNotice && (
        <div className="pointer-events-auto w-full max-w-3xl mb-2 bg-amber-50/95 backdrop-blur-md border border-amber-300/80 rounded-xl p-3 sm:p-4 shadow-lg text-ink-900 animate-in fade-in slide-in-from-bottom-2 duration-200">
          <div className="flex items-start justify-between gap-2">
            <div className="flex items-start gap-2">
              <Info className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
              <div>
                <p className="text-xs font-semibold text-amber-900 leading-snug">
                  {demoNotice.message}
                </p>
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {demoNotice.suggestions.map((s, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => handleChipClick(s.query)}
                      className="px-2.5 py-1 text-[11px] font-medium bg-white hover:bg-amber-100/60 text-amber-900 border border-amber-300/80 rounded-md transition-colors shadow-xs cursor-pointer"
                    >
                      {s.text} →
                    </button>
                  ))}
                </div>
              </div>
            </div>
            <button
              type="button"
              onClick={onClearDemoNotice}
              className="p-1 rounded hover:bg-amber-200/50 text-amber-800 transition-colors cursor-pointer"
              aria-label="Dismiss notice"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* Main Unified Input Container */}
      <div className="pointer-events-auto w-full max-w-3xl flex flex-col gap-1.5">
        {/* Suggestion Chips */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar px-1">
          <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-ink-500 shrink-0 flex items-center gap-1">
            <Sparkles className="w-2.5 h-2.5 text-sky-600" />
            Suggested Topics:
          </span>
          {sampleChips.map((chip, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleChipClick(chip.query)}
              disabled={isGenerating}
              className="shrink-0 px-2.5 py-0.5 text-[11px] font-medium rounded-full bg-white/90 hover:bg-white text-ink-700 hover:text-sky-900 border border-paper-300 hover:border-sky-300 shadow-paper-sm transition-all hover:scale-[1.02] cursor-pointer disabled:opacity-50"
            >
              {chip.label}
            </button>
          ))}
        </div>

        {/* Input Bar Form */}
        <form
          onSubmit={handleSubmit}
          className={`
            relative bg-white/95 backdrop-blur-md rounded-2xl border border-paper-300/90 shadow-paper-lg p-1.5 sm:p-2 flex items-center gap-2
            focus-within:border-sky-500 focus-within:ring-2 focus-within:ring-sky-500/20 transition-all
            ${isTransitioning || isGenerating ? 'opacity-90' : 'opacity-100'}
          `}
        >
          {/* Left Affordances: Upload Image + Attach Attempt */}
          <div className="flex items-center gap-0.5 shrink-0 pl-1">
            {/* Upload Question Image */}
            <div className="relative">
              <button
                type="button"
                onClick={() => setActiveTooltip((prev) => (prev === 'image' ? null : 'image'))}
                onMouseEnter={() => setActiveTooltip('image')}
                onMouseLeave={() => setActiveTooltip(null)}
                className="p-1.5 rounded-lg hover:bg-paper-100 text-ink-600 hover:text-ink-900 transition-colors cursor-pointer"
                title="Attach question image (Multimodal in Phase 5)"
                aria-label="Attach question image"
              >
                <ImageIcon className="w-4 h-4" />
              </button>
              {activeTooltip === 'image' && (
                <div className="absolute bottom-full left-0 mb-2 px-2.5 py-1 text-[11px] font-mono text-white bg-ink-900 rounded shadow-md whitespace-nowrap z-50">
                  Question Image Scan (Phase 5)
                </div>
              )}
            </div>

            {/* Attach Student Attempt */}
            <div className="relative">
              <button
                type="button"
                onClick={() => setActiveTooltip((prev) => (prev === 'attempt' ? null : 'attempt'))}
                onMouseEnter={() => setActiveTooltip('attempt')}
                onMouseLeave={() => setActiveTooltip(null)}
                className="p-1.5 rounded-lg hover:bg-paper-100 text-ink-600 hover:text-ink-900 transition-colors cursor-pointer"
                title="Attach handwritten student attempt"
                aria-label="Attach handwritten attempt"
              >
                <FileEdit className="w-4 h-4" />
              </button>
              {activeTooltip === 'attempt' && (
                <div className="absolute bottom-full left-0 mb-2 px-2.5 py-1 text-[11px] font-mono text-white bg-ink-900 rounded shadow-md whitespace-nowrap z-50">
                  Attach Student Work (Phase 5)
                </div>
              )}
            </div>
          </div>

          {/* Text Input Field */}
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isGenerating}
            placeholder={
              isGenerating
                ? "Building your explanation…"
                : "Ask anything you're stuck on... (e.g. 'why is friction acting downward', 'sn1 vs sn2')"
            }
            className="flex-1 bg-transparent border-0 text-xs sm:text-sm text-ink-900 placeholder:text-ink-400 focus:outline-none focus:ring-0 py-1.5 px-1 font-sans disabled:text-ink-500"
            aria-label="Ask a JEE question"
          />

          {/* Right Actions: Voice + Submit */}
          <div className="flex items-center gap-1 shrink-0 pr-0.5">
            {/* Voice Input (Disabled for Phase 1) */}
            <div className="relative">
              <button
                type="button"
                onClick={() => setActiveTooltip((prev) => (prev === 'voice' ? null : 'voice'))}
                onMouseEnter={() => setActiveTooltip('voice')}
                onMouseLeave={() => setActiveTooltip(null)}
                className="p-1.5 rounded-lg hover:bg-paper-100 text-ink-400 hover:text-ink-600 transition-colors relative cursor-pointer"
                title="Voice interaction (Post-V1 capability)"
                aria-label="Voice interaction"
              >
                <Mic className="w-4 h-4" />
                <span className="absolute -top-1 -right-1 text-[8px] font-mono font-bold px-1 rounded bg-paper-200 text-ink-500 border border-paper-300">
                  V2
                </span>
              </button>
              {activeTooltip === 'voice' && (
                <div className="absolute bottom-full right-0 mb-2 px-2.5 py-1 text-[11px] font-mono text-white bg-ink-900 rounded shadow-md whitespace-nowrap z-50">
                  Voice Interaction (Deferred to V2)
                </div>
              )}
            </div>

            {/* Send / Loading Button */}
            <button
              type="submit"
              disabled={isGenerating || !inputValue.trim()}
              className={`
                p-2 rounded-xl flex items-center justify-center transition-all shadow-xs
                ${
                  isGenerating
                    ? 'bg-sky-600 text-white cursor-wait'
                    : inputValue.trim()
                    ? 'bg-sky-600 hover:bg-sky-700 text-white cursor-pointer hover:scale-105 active:scale-95'
                    : 'bg-paper-200 text-ink-400 cursor-not-allowed'
                }
              `}
              title={isGenerating ? "Building explanation..." : "Compose Digital Study Sheet"}
              aria-label="Send Query"
            >
              {isGenerating ? (
                <RefreshCw className="w-4 h-4 animate-spin text-white" />
              ) : (
                <Send className="w-4 h-4" />
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

