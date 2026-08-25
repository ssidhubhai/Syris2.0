import React from 'react';
import { ExplanationDocument } from '@/types/explanation';
import { ZoomIn, ZoomOut, Code, Focus, History, Menu, Sparkles } from 'lucide-react';

interface WorkspaceHeaderProps {
  document: ExplanationDocument;
  zoomScale: number;
  zoomIn: () => void;
  zoomOut: () => void;
  resetZoom: () => void;
  focusedNodeId: string | null;
  onClearFocus: () => void;
  onToggleHistory: () => void;
  isHistoryOpen: boolean;
  onToggleSidebar: () => void;
  onOpenInspector: () => void;
}

export const WorkspaceHeader: React.FC<WorkspaceHeaderProps> = ({
  document,
  zoomScale,
  zoomIn,
  zoomOut,
  resetZoom,
  focusedNodeId,
  onClearFocus,
  onToggleHistory,
  isHistoryOpen,
  onToggleSidebar,
  onOpenInspector,
}) => {
  const getSubjectBadgeStyle = (subject: string) => {
    switch (subject.toLowerCase()) {
      case 'physics':
        return 'bg-sky-50 text-sky-800 border-sky-200';
      case 'chemistry':
        return 'bg-purple-50 text-purple-800 border-purple-200';
      case 'mathematics':
      case 'maths':
      case 'math':
        return 'bg-amber-50 text-amber-800 border-amber-200';
      default:
        return 'bg-paper-100 text-ink-700 border-paper-300';
    }
  };

  return (
    <header
      className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-paper-300 px-3 sm:px-6 py-2.5 flex items-center justify-between shadow-paper-sm select-none"
      role="banner"
    >
      {/* Left: Mobile menu toggle + Brand & Subject Context */}
      <div className="flex items-center gap-2.5 sm:gap-3 min-w-0">
        <button
          type="button"
          onClick={onToggleSidebar}
          className="p-1.5 rounded hover:bg-paper-100 text-ink-700 md:hidden transition-colors"
          aria-label="Toggle navigation menu"
          title="Toggle Navigation Menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-md bg-[#16202C] text-white flex items-center justify-center font-bold text-xs shadow-sm font-mono tracking-tighter">
            SY
          </div>
          <div className="hidden sm:flex flex-col">
            <span className="text-xs font-bold tracking-tight text-ink-900 leading-none">
              SYRIS
            </span>
            <span className="text-[10px] font-mono font-medium text-ink-400 leading-tight">
              AI JEE Companion
            </span>
          </div>
        </div>

        <div className="h-5 w-[1px] bg-paper-300 mx-1 hidden sm:block" />

        <div className="min-w-0 flex flex-col justify-center">
          <div className="flex items-center gap-1.5">
            <span
              className={`text-[10px] font-mono font-bold uppercase tracking-wider px-1.5 py-0.5 rounded border leading-none ${getSubjectBadgeStyle(
                document.subject
              )}`}
            >
              {document.subject}
            </span>
            <span className="text-[10px] text-ink-400 hidden sm:inline font-mono">
              • Digital Study Sheet
            </span>
          </div>
          <h1 className="text-xs sm:text-sm font-bold text-ink-900 truncate max-w-xs sm:max-w-md md:max-w-lg mt-0.5">
            {document.title}
          </h1>
        </div>
      </div>

      {/* Right: Actions (Focus Reset, Zoom Controls, History, Dev Tools) */}
      <div className="flex items-center gap-1.5 sm:gap-2 shrink-0">
        {focusedNodeId && (
          <button
            type="button"
            onClick={onClearFocus}
            className="flex items-center gap-1 px-2.5 py-1 text-xs font-mono font-semibold text-sky-700 bg-sky-50 border border-sky-200 rounded shadow-sm hover:bg-sky-100 transition-colors"
            title="Clear Step Focus Mode"
          >
            <Focus className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Clear Focus</span>
          </button>
        )}

        {/* Zoom Controls */}
        <div className="flex items-center bg-paper-50 rounded border border-paper-300 p-0.5 shadow-sm">
          <button
            type="button"
            onClick={zoomOut}
            className="p-1 rounded hover:bg-paper-200 text-ink-700 transition-colors"
            title="Zoom Out"
            aria-label="Zoom Out"
          >
            <ZoomOut className="w-3.5 h-3.5" />
          </button>
          <button
            type="button"
            onClick={resetZoom}
            className="px-1.5 sm:px-2 py-0.5 text-[11px] sm:text-xs font-mono font-semibold text-ink-800 hover:bg-paper-200 transition-colors"
            title="Reset Zoom"
          >
            {Math.round(zoomScale * 100)}%
          </button>
          <button
            type="button"
            onClick={zoomIn}
            className="p-1 rounded hover:bg-paper-200 text-ink-700 transition-colors"
            title="Zoom In"
            aria-label="Zoom In"
          >
            <ZoomIn className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* History Toggle Button */}
        <button
          type="button"
          onClick={onToggleHistory}
          className={`flex items-center gap-1.5 px-2.5 py-1 text-xs font-mono font-medium rounded border transition-colors shadow-sm ${
            isHistoryOpen
              ? 'bg-sky-50 text-sky-800 border-sky-300'
              : 'bg-paper-50 text-ink-700 border-paper-300 hover:bg-paper-200 hover:text-ink-900'
          }`}
          title="Toggle Study Session History"
          aria-label="Toggle History"
        >
          <History className="w-3.5 h-3.5" />
          <span className="hidden md:inline">History</span>
        </button>

        {/* Dev Inspector Trigger */}
        <button
          type="button"
          onClick={onOpenInspector}
          className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-mono font-medium text-ink-700 bg-paper-50 border border-paper-300 rounded hover:bg-paper-200 hover:text-ink-900 transition-colors shadow-sm"
          title="Inspect ExplanationDocument Schema & Fixtures"
          aria-label="Dev Tools"
        >
          <Code className="w-3.5 h-3.5 text-ink-600" />
          <span className="hidden lg:inline">Dev Tools</span>
        </button>
      </div>
    </header>
  );
};
