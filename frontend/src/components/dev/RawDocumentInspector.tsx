import React, { useState } from 'react';
import { ExplanationDocument } from '@/types/explanation';
import { DEV_FIXTURES } from '@/fixtures';
import { Code, X, Copy, Check, Layers, Server, RefreshCw, Sparkles } from 'lucide-react';
import { syrisApi } from '@/services/apiClient';
import { DevSmokeTestPanel } from './DevSmokeTestPanel';

interface RawDocumentInspectorProps {
  document: ExplanationDocument;
  isOpen: boolean;
  onClose: () => void;
  onSelectFixture?: (key: string) => void;
  activeFixtureKey?: string;
}

export const RawDocumentInspector: React.FC<RawDocumentInspectorProps> = ({
  document: doc,
  isOpen,
  onClose,
  onSelectFixture,
  activeFixtureKey = 'canonical_physics',
}) => {
  const [activeTab, setActiveTab] = useState<'document' | 'gemini_smoke'>('document');
  const [copied, setCopied] = useState(false);
  const [backendSyncStatus, setBackendSyncStatus] = useState<string | null>(null);
  const [isSyncing, setIsSyncing] = useState(false);


  if (!isOpen) return null;

  const jsonString = JSON.stringify(doc, null, 2);

  const handleCopy = () => {
    navigator.clipboard.writeText(jsonString);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleBackendSync = async () => {
    try {
      setIsSyncing(true);
      setBackendSyncStatus('Connecting to backend...');
      
      const session = await syrisApi.createSession({
        title: doc.title,
        subject: doc.subject,
      });

      await syrisApi.appendMessage(session.id, {
        role: 'user',
        content: `Dev Inspector Sync for ${doc.title}`,
      });

      const syncedDoc = {
        ...doc,
        session_id: session.id,
      };

      await syrisApi.saveExplanation(session.id, syncedDoc);
      setBackendSyncStatus(`Synced to DB! Session ID: ${session.id}`);
    } catch (err: any) {
      setBackendSyncStatus(`Backend Offline / Error: ${err.error?.message || err.message}`);
    } finally {
      setIsSyncing(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex justify-end animate-fadeIn" data-testid="raw-inspector-modal">
      <div className="w-full max-w-2xl bg-ink-900 text-paper-100 h-full shadow-2xl flex flex-col">
        <div className="p-4 border-b border-ink-700 flex items-center justify-between bg-ink-800">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <Code className="w-4 h-4 text-academic-physics-accent" />
              <h3 className="text-sm font-mono font-bold text-white">
                Dev Tools & Diagnostics
              </h3>
            </div>

            {/* Dev Tabs */}
            <div className="flex items-center bg-ink-950 p-0.5 rounded border border-ink-700 text-xs font-mono">
              <button
                type="button"
                onClick={() => setActiveTab('document')}
                className={`px-2.5 py-1 rounded transition-colors ${
                  activeTab === 'document'
                    ? 'bg-ink-700 text-white font-bold'
                    : 'text-ink-400 hover:text-white'
                }`}
                data-testid="tab-document-json"
              >
                Document JSON
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('gemini_smoke')}
                className={`px-2.5 py-1 rounded flex items-center gap-1.5 transition-colors ${
                  activeTab === 'gemini_smoke'
                    ? 'bg-academic-physics-accent text-white font-bold'
                    : 'text-ink-400 hover:text-white'
                }`}
                data-testid="tab-gemini-smoke"
              >
                <Sparkles className="w-3 h-3" />
                <span>Gemini Smoke</span>
              </button>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {activeTab === 'document' && (
              <>
                <button
                  type="button"
                  onClick={handleBackendSync}
                  disabled={isSyncing}
                  className="p-1.5 rounded bg-emerald-800 hover:bg-emerald-700 text-emerald-100 text-xs font-mono flex items-center gap-1 transition-colors"
                  title="Test Persisting this ExplanationDocument to Backend API"
                >
                  {isSyncing ? (
                    <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  ) : (
                    <Server className="w-3.5 h-3.5 text-emerald-300" />
                  )}
                  <span>{isSyncing ? 'Syncing...' : 'Sync to Backend'}</span>
                </button>
                <button
                  type="button"
                  onClick={handleCopy}
                  className="p-1.5 rounded bg-ink-700 hover:bg-ink-500 text-xs font-mono flex items-center gap-1 transition-colors"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? 'Copied!' : 'Copy JSON'}</span>
                </button>
              </>
            )}
            <button
              type="button"
              onClick={onClose}
              className="p-1.5 rounded bg-ink-700 hover:bg-ink-500 transition-colors"
              aria-label="Close Inspector"
            >
              <X className="w-4 h-4 text-white" />
            </button>
          </div>
        </div>

        {activeTab === 'gemini_smoke' ? (
          <div className="flex-1 overflow-auto p-2">
            <DevSmokeTestPanel />
          </div>
        ) : (
          <>
            {backendSyncStatus && (
              <div className="px-4 py-2 bg-ink-950 border-b border-ink-700 text-[11px] font-mono text-emerald-400 flex items-center gap-2">
                <Server className="w-3 h-3 text-emerald-400 shrink-0" />
                <span className="truncate">{backendSyncStatus}</span>
              </div>
            )}

            {/* Development Pattern Showcase Switcher */}
            {onSelectFixture && (
              <div className="px-4 py-3 bg-ink-800/90 border-b border-ink-700">
                <div className="flex items-center gap-1.5 text-xs font-mono text-ink-400 mb-2">
                  <Layers className="w-3.5 h-3.5 text-academic-physics-accent" />
                  <span>Dev Pattern Showcase (Select Fixture to Verify Composition):</span>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  {Object.entries(DEV_FIXTURES).map(([key, item]) => (
                    <button
                      key={key}
                      type="button"
                      onClick={() => onSelectFixture(key)}
                      className={`p-2 rounded text-left text-xs font-mono border transition-all ${
                        activeFixtureKey === key
                          ? 'bg-academic-physics-accent/20 border-academic-physics-accent text-white font-bold'
                          : 'bg-ink-700/50 border-ink-600 text-ink-300 hover:bg-ink-700'
                      }`}
                    >
                      <div className="text-[11px] text-academic-physics-border">{item.pattern}</div>
                      <div className="truncate">{item.label}</div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="px-4 py-2 bg-ink-800/50 border-b border-ink-700 text-xs font-mono flex gap-4 text-ink-300">
              <div>Subject: <span className="text-academic-physics-border">{doc.subject}</span></div>
              <div>Nodes: <span className="text-white">{doc.nodes.length}</span></div>
              <div>Relations: <span className="text-white">{doc.relationships.length}</span></div>
            </div>

            <div className="p-4 flex-1 overflow-auto">
              <pre className="text-xs font-mono leading-relaxed text-emerald-300 whitespace-pre">
                {jsonString}
              </pre>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

