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
  onOpenInspector?: () => void;
  isDevMode?: boolean;
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
  isDevMode = false,
}) => {
  const getSubjectBadgeStyle = (subject: string) => {
    switch (subject.toLowerCase()) {
      case 'physics':
        return 'text-sky-700 bg-sky-50 border-sky-200';
      case 'chemistry':
        return 'text-purple-700 bg-purple-50 border-purple-200';
      case 'mathematics':
      case 'maths':
      case 'math':
        return 'text-amber-700 bg-amber-50 border-amber-200';
      default:
        return 'text-ink-700 bg-paper-100 border-[#E5E3D8]';
    }
  };

  return (
    <header
      className="sticky top-0 z-40 bg-[#FDFCFB]/95 backdrop-blur-md border-b border-[#E8E5DC] px-3 sm:px-6 py-2 flex items-center justify-between select-none shadow-xs"
      role="banner"
    >
      {/* Left: Mobile menu toggle + Brand & Subject Context */}
      <div className="flex items-center gap-2.5 sm:gap-3 min-w-0">
        <button
          type="button"
          onClick={onToggleSidebar}
          className="p-1 rounded hover:bg-paper-100 text-ink-700 md:hidden transition-colors"
          aria-label="Toggle navigation menu"
          title="Toggle Navigation Menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-1.5">
          <span className="font-bold text-xs font-mono tracking-tight text-ink-950 bg-paper-200/80 px-1.5 py-0.5 rounded border border-[#D5D2C7]">
            SYRIS
          </span>
        </div>

        <div className="h-4 w-[1px] bg-[#E8E5DC] mx-0.5 hidden sm:block" />

        <div className="min-w-0 flex items-center gap-2">
          <span
            className={`text-[10px] font-mono font-semibold uppercase tracking-wider px-1.5 py-0.5 rounded border leading-none shrink-0 ${getSubjectBadgeStyle(
              document.subject
            )}`}
          >
            {document.subject}
          </span>
          <h1 className="text-xs sm:text-sm font-medium text-ink-800 truncate max-w-xs sm:max-w-md md:max-w-lg">
            {document.title}
          </h1>
        </div>
      </div>

      {/* Right: Actions (Focus Reset, Zoom Controls, History, Optional Dev Tools) */}
      <div className="flex items-center gap-1.5 sm:gap-2 shrink-0">
        {focusedNodeId && (
          <button
            type="button"
            onClick={onClearFocus}
            className="flex items-center gap-1 px-2 py-0.5 text-xs font-mono font-medium text-sky-700 bg-sky-50 border border-sky-200 rounded hover:bg-sky-100 transition-colors"
            title="Clear Step Focus Mode"
          >
            <Focus className="w-3 h-3" />
            <span className="hidden sm:inline">Clear Focus</span>
          </button>
        )}

        {/* Zoom Controls */}
        <div className="flex items-center bg-paper-100/80 rounded border border-[#E5E3D8] p-0.5">
          <button
            type="button"
            onClick={zoomOut}
            className="p-1 rounded hover:bg-paper-200 text-ink-600 transition-colors"
            title="Zoom Out"
            aria-label="Zoom Out"
          >
            <ZoomOut className="w-3.5 h-3.5" />
          </button>
          <button
            type="button"
            onClick={resetZoom}
            className="px-1.5 py-0.5 text-[11px] font-mono font-semibold text-ink-700 hover:bg-paper-200 transition-colors"
            title="Reset Zoom"
          >
            {Math.round(zoomScale * 100)}%
          </button>
          <button
            type="button"
            onClick={zoomIn}
            className="p-1 rounded hover:bg-paper-200 text-ink-600 transition-colors"
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
          className={`flex items-center gap-1.5 px-2.5 py-1 text-xs font-mono font-medium rounded border transition-colors ${
            isHistoryOpen
              ? 'bg-sky-50 text-sky-800 border-sky-300'
              : 'bg-paper-100/80 text-ink-700 border-[#E5E3D8] hover:bg-paper-200 hover:text-ink-900'
          }`}
          title="Toggle Study Session History"
          aria-label="Toggle History"
        >
          <History className="w-3.5 h-3.5" />
          <span className="hidden md:inline">History</span>
        </button>

        {/* Dev Inspector Trigger (Only visible when explicit dev mode is enabled) */}
        {isDevMode && onOpenInspector && (
          <button
            type="button"
            onClick={onOpenInspector}
            className="flex items-center gap-1 px-2 py-1 text-xs font-mono font-medium text-ink-600 bg-paper-100 border border-[#E5E3D8] rounded hover:bg-paper-200 hover:text-ink-900 transition-colors"
            title="Inspect ExplanationDocument Schema & Fixtures"
            aria-label="Dev Tools"
          >
            <Code className="w-3.5 h-3.5 text-ink-600" />
            <span className="hidden lg:inline">Dev Tools</span>
          </button>
        )}
      </div>
    </header>
  );
};
