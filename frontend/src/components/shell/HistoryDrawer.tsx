import React from 'react';
import { HistorySessionItem } from '@/hooks/useStudyWorkspaceSession';
import { X, Clock, ArrowRight, BookOpen, Layers } from 'lucide-react';

interface HistoryDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  historyItems: HistorySessionItem[];
  activeFixtureKey: string;
  onRestoreSession: (sessionId: string) => void;
}

export const HistoryDrawer: React.FC<HistoryDrawerProps> = ({
  isOpen,
  onClose,
  historyItems,
  activeFixtureKey,
  onRestoreSession,
}) => {
  if (!isOpen) return null;

  const getSubjectColor = (subject: string) => {
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
        return 'text-ink-700 bg-paper-100 border-paper-300';
    }
  };

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-ink-900/20 backdrop-blur-xs z-50 transition-opacity"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Drawer */}
      <div
        className="fixed top-0 right-0 bottom-0 w-full sm:w-96 bg-white z-50 shadow-2xl border-l border-paper-300 flex flex-col animate-in slide-in-from-right duration-200"
        role="dialog"
        aria-label="Study Session History"
      >
        {/* Header */}
        <div className="p-4 border-b border-paper-200 flex items-center justify-between bg-paper-50/70">
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-ink-700" />
            <h2 className="text-sm font-bold text-ink-900 font-mono tracking-tight">
              STUDY SESSIONS
            </h2>
            <span className="text-[10px] font-mono font-semibold px-1.5 py-0.5 rounded bg-paper-200 text-ink-600 border border-paper-300">
              {historyItems.length}
            </span>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-1.5 rounded hover:bg-paper-200 text-ink-600 transition-colors"
            aria-label="Close history drawer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* List of Sessions */}
        <div className="flex-1 overflow-y-auto p-3 space-y-2.5">
          {historyItems.map((item) => {
            const isActive = activeFixtureKey === item.fixtureKey;
            return (
              <div
                key={item.id}
                onClick={() => {
                  onRestoreSession(item.id);
                  onClose();
                }}
                className={`
                  group p-3 rounded-lg border text-left cursor-pointer transition-all
                  ${
                    isActive
                      ? 'bg-sky-50/70 border-sky-300 ring-1 ring-sky-300/50 shadow-xs'
                      : 'bg-paper-50/50 hover:bg-paper-100/80 border-paper-200 hover:border-paper-300 hover:shadow-xs'
                  }
                `}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    onRestoreSession(item.id);
                    onClose();
                  }
                }}
              >
                <div className="flex items-center justify-between gap-2 mb-1.5">
                  <span
                    className={`text-[9px] font-mono font-bold uppercase tracking-wider px-1.5 py-0.2 rounded border ${getSubjectColor(
                      item.subject
                    )}`}
                  >
                    {item.subject}
                  </span>
                  <span className="text-[10px] text-ink-400 font-mono">{item.timestamp}</span>
                </div>

                <h3 className="text-xs font-bold text-ink-900 group-hover:text-sky-900 line-clamp-1 mb-1">
                  {item.title}
                </h3>

                <p className="text-[11px] text-ink-600 line-clamp-2 italic font-serif">
                  &ldquo;{item.query}&rdquo;
                </p>

                <div className="mt-2.5 pt-2 border-t border-paper-200/80 flex items-center justify-between text-[10px] font-mono text-ink-500">
                  <div className="flex items-center gap-1">
                    <Layers className="w-3 h-3 text-ink-400" />
                    <span>{item.document.nodes.length} nodes</span>
                  </div>
                  <span className="flex items-center gap-1 text-sky-700 font-semibold group-hover:translate-x-0.5 transition-transform">
                    {isActive ? 'Active Sheet' : 'Restore Sheet'}
                    <ArrowRight className="w-3 h-3" />
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Footer info */}
        <div className="p-3 border-t border-paper-200 bg-paper-50/50 text-[11px] text-ink-500 font-mono flex items-center justify-between">
          <span>In-memory demo state</span>
          <span>Phase 1B Shell</span>
        </div>
      </div>
    </>
  );
};
