import { useState, useCallback, useEffect } from 'react';
import { ExplanationDocument } from '@/types/explanation';
import { DEV_FIXTURES, matchDemoFixture, FixtureEntry } from '@/fixtures';
import { REGRESSION_FIXTURES } from '@/fixtures/regression';
import { syrisApi } from '@/services/apiClient';

export interface HistorySessionItem {
  id: string;
  title: string;
  subject: 'physics' | 'chemistry' | 'mathematics' | 'general';
  query: string;
  timestamp: string;
  fixtureKey: string;
  document: ExplanationDocument;
  backendSynced?: boolean;
}

export interface DemoNotice {
  message: string;
  suggestions: { text: string; query: string }[];
}

export const INITIAL_DEMO_SESSIONS: HistorySessionItem[] = [
  {
    id: 'sess-demo-physics-wedge',
    title: 'Wedge Incline with Static Friction & Pseudo Force',
    subject: 'physics',
    query: 'Why is friction acting downward on the wedge?',
    timestamp: 'Just now',
    fixtureKey: 'canonical_physics',
    document: DEV_FIXTURES.canonical_physics.doc,
  },
  {
    id: 'sess-demo-concept-potential',
    title: 'Electric Potential as a Path-Independent Scalar Field',
    subject: 'physics',
    query: 'Why is electric potential a scalar quantity?',
    timestamp: '15m ago',
    fixtureKey: 'concept_physics',
    document: DEV_FIXTURES.concept_physics.doc,
  },
  {
    id: 'sess-demo-chem-sn1-sn2',
    title: 'Bimolecular (SN2) vs Unimolecular (SN1) Substitution',
    subject: 'chemistry',
    query: 'How to decide between SN1 and SN2 mechanisms?',
    timestamp: '1h ago',
    fixtureKey: 'chemistry_comparison',
    document: DEV_FIXTURES.chemistry_comparison.doc,
  },
  {
    id: 'sess-demo-math-feynman',
    title: "Frullani Definite Integral via Feynman's Trick",
    subject: 'mathematics',
    query: "Evaluate definite integral using Feynman's trick",
    timestamp: '2h ago',
    fixtureKey: 'canonical_math',
    document: DEV_FIXTURES.canonical_math.doc,
  },
  {
    id: 'sess-demo-kinematics-centripetal',
    title: 'Uniform Circular Motion Centripetal Acceleration',
    subject: 'physics',
    query: 'What is centripetal acceleration and how to derive it?',
    timestamp: 'Yesterday',
    fixtureKey: 'compact_definition',
    document: DEV_FIXTURES.compact_definition.doc,
  },
];

export function useStudyWorkspaceSession(initialFixtureKey = 'canonical_physics') {
  const [activeFixtureKey, setActiveFixtureKey] = useState<string>(initialFixtureKey);
  const [activeDocument, setActiveDocument] = useState<ExplanationDocument>(
    DEV_FIXTURES[initialFixtureKey]?.doc || DEV_FIXTURES.canonical_physics.doc
  );
  const [currentQuery, setCurrentQuery] = useState<string>(
    DEV_FIXTURES[initialFixtureKey]?.sampleQuery || ''
  );
  const [historyItems, setHistoryItems] = useState<HistorySessionItem[]>(INITIAL_DEMO_SESSIONS);
  const [isTransitioning, setIsTransitioning] = useState<boolean>(false);
  const [demoNotice, setDemoNotice] = useState<DemoNotice | null>(null);
  
  // Backend synchronization state
  const [backendSessionId, setBackendSessionId] = useState<string | null>(null);
  const [backendSyncStatus, setBackendSyncStatus] = useState<'idle' | 'syncing' | 'synced' | 'offline' | 'error'>('idle');

  // Attempt backend persistence for a document and query
  const syncToBackend = useCallback(async (doc: ExplanationDocument, query: string) => {
    try {
      setBackendSyncStatus('syncing');
      
      // 1. Create or use existing backend session
      const sessionRes = await syrisApi.createSession({
        title: doc.title,
        subject: doc.subject,
      });

      const sessId = sessionRes.id;
      setBackendSessionId(sessId);

      // 2. Persist user query message if present
      if (query) {
        await syrisApi.appendMessage(sessId, {
          role: 'user',
          content: query,
        });
      }

      // 3. Persist canonical explanation document with updated session_id
      const docToPersist = {
        ...doc,
        session_id: sessId,
      };
      await syrisApi.saveExplanation(sessId, docToPersist);

      setBackendSyncStatus('synced');
      return sessId;
    } catch {
      setBackendSyncStatus('offline');
      return null;
    }
  }, []);

  const applyFixture = useCallback((entry: FixtureEntry, customQuery?: string) => {
    setIsTransitioning(true);
    setActiveFixtureKey(entry.key);
    setActiveDocument(entry.doc);
    const queryToUse = customQuery || entry.sampleQuery;
    setCurrentQuery(queryToUse);
    setDemoNotice(null);

    // Update local history
    setHistoryItems((prev) => {
      const existsIndex = prev.findIndex((item) => item.fixtureKey === entry.key);
      const updatedItem: HistorySessionItem = {
        id: `sess-${entry.key}-${Date.now()}`,
        title: entry.doc.title,
        subject: entry.subject,
        query: queryToUse,
        timestamp: 'Just now',
        fixtureKey: entry.key,
        document: entry.doc,
      };

      if (existsIndex >= 0) {
        const copy = [...prev];
        copy.splice(existsIndex, 1);
        return [updatedItem, ...copy];
      }
      return [updatedItem, ...prev];
    });

    // Fire non-blocking backend sync
    syncToBackend(entry.doc, queryToUse).catch(() => {});

    setTimeout(() => {
      setIsTransitioning(false);
    }, 150);
  }, [syncToBackend]);

  const [isGenerating, setIsGenerating] = useState<boolean>(false);

  const submitQuery = useCallback(
    async (query: string) => {
      const trimmed = query.trim();
      if (!trimmed) return;

      setIsGenerating(true);
      setCurrentQuery(trimmed);
      setDemoNotice(null);

      try {
        const response = await syrisApi.askStudyQuestion({
          session_id: backendSessionId,
          message: trimmed,
        });

        const doc = response.explanation_document;
        setBackendSessionId(response.session_id);
        setActiveDocument(doc);
        setActiveFixtureKey('real_ai_generated');

        // Add to history
        const newHistoryItem: HistorySessionItem = {
          id: response.session_id,
          title: doc.title || trimmed,
          subject: doc.subject as any,
          query: trimmed,
          timestamp: 'Just now',
          fixtureKey: 'real_ai_generated',
          document: doc,
          backendSynced: true,
        };

        setHistoryItems((prev) => [newHistoryItem, ...prev.filter((i) => i.id !== response.session_id)]);
      } catch (err: any) {
        // If live API fails, display friendly student banner
        const errMsg = err?.error?.message || 'Could not connect to AI study companion. Please check backend status.';
        setDemoNotice({
          message: `${errMsg} You can continue exploring using the verified demo topics below:`,
          suggestions: [
            { text: 'Wedge Incline Friction', query: 'Why is friction acting downward on the wedge?' },
            { text: 'Electric Potential Scalar', query: 'Why is electric potential a scalar quantity?' },
            { text: 'SN1 vs SN2 Mechanisms', query: 'How to decide between SN1 and SN2 mechanisms?' },
            { text: 'Centripetal Acceleration', query: 'What is centripetal acceleration?' },
            { text: "Feynman's Integral Trick", query: "Evaluate definite integral using Feynman's trick" },
          ],
        });
      } finally {
        setIsGenerating(false);
      }
    },
    [backendSessionId]
  );

  const restoreHistorySession = useCallback(async (sessionId: string) => {
    // Check local history first
    const item = historyItems.find((s) => s.id === sessionId);
    if (item) {
      setIsTransitioning(true);
      setActiveFixtureKey(item.fixtureKey);
      setActiveDocument(item.document);
      setCurrentQuery(item.query);
      setBackendSessionId(item.id.startsWith('sess-demo-') ? null : item.id);
      setDemoNotice(null);
      setTimeout(() => {
        setIsTransitioning(false);
      }, 150);
      return;
    }

    // Try backend restoration if not found locally
    try {
      setIsTransitioning(true);
      const backendSession = await syrisApi.getSession(sessionId);
      if (backendSession.latest_explanation?.document_json) {
        const restoredDoc = backendSession.latest_explanation.document_json;
        setActiveDocument(restoredDoc);
        setBackendSessionId(backendSession.id);
        const lastMsg = backendSession.messages?.[0]?.content || '';
        setCurrentQuery(lastMsg);
      }
    } catch {
      // Graceful ignore
    } finally {
      setIsTransitioning(false);
    }
  }, [historyItems]);

  const selectFixture = useCallback((fixtureKey: string) => {
    const entry = DEV_FIXTURES[fixtureKey];
    if (entry) {
      applyFixture(entry);
      return;
    }
    const regDoc = REGRESSION_FIXTURES[fixtureKey];
    if (regDoc) {
      setIsTransitioning(true);
      setActiveFixtureKey(fixtureKey);
      setActiveDocument(regDoc);
      setCurrentQuery(regDoc.title || '');
      setDemoNotice(null);
      setTimeout(() => {
        setIsTransitioning(false);
      }, 150);
    }
  }, [applyFixture]);

  const clearDemoNotice = useCallback(() => {
    setDemoNotice(null);
  }, []);

  return {
    activeDocument,
    activeFixtureKey,
    currentQuery,
    historyItems,
    isTransitioning,
    isGenerating,
    demoNotice,
    backendSessionId,
    backendSyncStatus,
    submitQuery,
    restoreHistorySession,
    selectFixture,
    clearDemoNotice,
    syncToBackend,
  };
}

