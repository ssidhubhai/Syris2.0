import React, { useState } from 'react';
import { ExplanationDocument } from '@/types/explanation';
import { DigitalPaperCanvas } from './DigitalPaperCanvas';
import { useJumpToReference } from '@/hooks/useJumpToReference';
import { usePaperZoom } from '@/hooks/usePaperZoom';
import { useStudyWorkspaceSession } from '@/hooks/useStudyWorkspaceSession';
import { RawDocumentInspector } from '../dev/RawDocumentInspector';
import { WorkspaceHeader } from '../shell/WorkspaceHeader';
import { WorkspaceSidebar, NavSection } from '../shell/WorkspaceSidebar';
import { HistoryDrawer } from '../shell/HistoryDrawer';
import { UnifiedInputBar } from '../shell/UnifiedInputBar';

interface DigitalPaperWorkspaceProps {
  initialFixtureKey?: string;
}

export const DigitalPaperWorkspace: React.FC<DigitalPaperWorkspaceProps> = ({
  initialFixtureKey = 'canonical_physics',
}) => {
  const {
    activeDocument,
    activeFixtureKey,
    currentQuery,
    historyItems,
    isTransitioning,
    isGenerating,
    demoNotice,
    submitQuery,
    restoreHistorySession,
    selectFixture,
    clearDemoNotice,
  } = useStudyWorkspaceSession(initialFixtureKey);

  const [currentSection, setCurrentSection] = useState<NavSection>('home');
  const [isHistoryOpen, setIsHistoryOpen] = useState<boolean>(false);
  const [isSidebarOpenMobile, setIsSidebarOpenMobile] = useState<boolean>(false);
  const [isSidebarCollapsedDesktop, setIsSidebarCollapsedDesktop] = useState<boolean>(false);
  const [isInspectorOpen, setIsInspectorOpen] = useState<boolean>(false);
  const [isDevMode, setIsDevMode] = useState<boolean>(false);
  const [focusedNodeId, setFocusedNodeId] = useState<string | null>(null);

  React.useEffect(() => {
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      setIsDevMode(params.get('dev') === 'true' || params.get('debug') === 'true');
      const fixtureParam = params.get('fixture') || params.get('case');
      if (fixtureParam) {
        selectFixture(fixtureParam);
      }
    }
  }, [selectFixture]);

  const { targetNodeId, jumpToNode } = useJumpToReference();
  const { zoomScale, zoomIn, zoomOut, resetZoom } = usePaperZoom();

  const handleToggleFocus = (nodeId: string | null) => {
    setFocusedNodeId((current) => (current === nodeId ? null : nodeId));
  };

  const handleSelectSection = (section: NavSection) => {
    setCurrentSection(section);
    if (section === 'history') {
      setIsHistoryOpen(true);
    }
  };

  return (
    <div className="min-h-screen bg-[#F4F3EE] text-ink-900 flex flex-col font-sans selection:bg-sky-100 selection:text-sky-900">
      {/* Workspace Header */}
      <WorkspaceHeader
        document={activeDocument}
        zoomScale={zoomScale}
        zoomIn={zoomIn}
        zoomOut={zoomOut}
        resetZoom={resetZoom}
        focusedNodeId={focusedNodeId}
        onClearFocus={() => setFocusedNodeId(null)}
        onToggleHistory={() => setIsHistoryOpen((prev) => !prev)}
        isHistoryOpen={isHistoryOpen}
        onToggleSidebar={() => setIsSidebarOpenMobile((prev) => !prev)}
        onOpenInspector={() => setIsInspectorOpen(true)}
        isDevMode={isDevMode}
      />

      {/* Main Workspace Layout (Sidebar + Canvas + Input) */}
      <div className="flex-1 flex overflow-hidden relative">
        {/* Minimal Navigation Sidebar */}
        <WorkspaceSidebar
          currentSection={currentSection}
          onSelectSection={handleSelectSection}
          isOpenMobile={isSidebarOpenMobile}
          onCloseMobile={() => setIsSidebarOpenMobile(false)}
          isCollapsedDesktop={isSidebarCollapsedDesktop}
          onToggleCollapseDesktop={() => setIsSidebarCollapsedDesktop((prev) => !prev)}
        />

        {/* Hero Digital Paper Area */}
        <main
          className={`flex-1 flex justify-center overflow-x-hidden overflow-y-auto pb-40 transition-opacity duration-150 ${
            isTransitioning ? 'opacity-40' : 'opacity-100'
          }`}
          role="main"
        >
          <DigitalPaperCanvas
            document={activeDocument}
            zoomScale={zoomScale}
            focusedNodeId={focusedNodeId}
            onFocusNode={handleToggleFocus}
            targetNodeId={targetNodeId}
            onJumpToReference={jumpToNode}
          />
        </main>
      </div>

      {/* Persistent Bottom Unified Input Bar */}
      <UnifiedInputBar
        currentQuery={currentQuery}
        onSubmitQuery={submitQuery}
        demoNotice={demoNotice}
        onClearDemoNotice={clearDemoNotice}
        isTransitioning={isTransitioning}
        isGenerating={isGenerating}
      />


      {/* Slide-out Study History Drawer */}
      <HistoryDrawer
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        historyItems={historyItems}
        activeFixtureKey={activeFixtureKey}
        onRestoreSession={restoreHistorySession}
      />

      {/* Developer Raw JSON & Fixture Inspector */}
      <RawDocumentInspector
        document={activeDocument}
        isOpen={isInspectorOpen}
        onClose={() => setIsInspectorOpen(false)}
        onSelectFixture={selectFixture}
        activeFixtureKey={activeFixtureKey}
      />
    </div>
  );
};
