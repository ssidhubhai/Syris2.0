import React from 'react';
import { Home, History, BookOpen, Target, AlertOctagon, ChevronLeft, ChevronRight, X } from 'lucide-react';

export type NavSection = 'home' | 'history' | 'practice' | 'concepts' | 'mistakes';

interface WorkspaceSidebarProps {
  currentSection: NavSection;
  onSelectSection: (section: NavSection) => void;
  isOpenMobile: boolean;
  onCloseMobile: () => void;
  isCollapsedDesktop: boolean;
  onToggleCollapseDesktop: () => void;
}

export const WorkspaceSidebar: React.FC<WorkspaceSidebarProps> = ({
  currentSection,
  onSelectSection,
  isOpenMobile,
  onCloseMobile,
  isCollapsedDesktop,
  onToggleCollapseDesktop,
}) => {
  const navItems = [
    {
      id: 'home' as NavSection,
      label: 'Study Sheet',
      icon: Home,
      badge: null,
      description: 'Active digital study workspace',
    },
    {
      id: 'history' as NavSection,
      label: 'History',
      icon: History,
      badge: null,
      description: 'Previous study sheets',
    },
    {
      id: 'practice' as NavSection,
      label: 'Practice',
      icon: Target,
      badge: 'V2',
      description: 'Adaptive problem drill',
    },
    {
      id: 'concepts' as NavSection,
      label: 'Concepts',
      icon: BookOpen,
      badge: 'V2',
      description: 'JEE concept graph',
    },
    {
      id: 'mistakes' as NavSection,
      label: 'Mistakes',
      icon: AlertOctagon,
      badge: 'V2',
      description: 'Mistake memory vault',
    },
  ];

  const handleNavClick = (section: NavSection) => {
    onSelectSection(section);
    if (isOpenMobile) {
      onCloseMobile();
    }
  };

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpenMobile && (
        <div
          className="fixed inset-0 bg-ink-900/30 backdrop-blur-sm z-40 md:hidden"
          onClick={onCloseMobile}
          aria-hidden="true"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`
          fixed md:sticky top-0 md:top-[41px] bottom-0 z-50 md:z-30
          bg-[#FDFCFB]/95 md:bg-[#FDFCFB]/80 backdrop-blur-md border-r border-[#E8E5DC]
          transition-all duration-200 ease-in-out flex flex-col justify-between
          ${isOpenMobile ? 'translate-x-0 w-64' : '-translate-x-full md:translate-x-0'}
          ${isCollapsedDesktop ? 'md:w-14' : 'md:w-52'}
          h-full md:h-[calc(100vh-41px)]
        `}
        aria-label="Workspace Navigation"
      >
        {/* Top Header (Mobile only close button) */}
        <div className="p-3 border-b border-[#E8E5DC] flex items-center justify-between md:hidden">
          <div className="flex items-center gap-2">
            <span className="font-bold text-xs font-mono text-ink-900">MENU</span>
          </div>
          <button
            type="button"
            onClick={onCloseMobile}
            className="p-1 rounded hover:bg-paper-100 text-ink-500"
            aria-label="Close sidebar"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Navigation List */}
        <div className="flex-1 py-3 px-2 space-y-0.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentSection === item.id;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => handleNavClick(item.id)}
                className={`
                  w-full flex items-center gap-3 px-2.5 py-1.5 rounded-md text-xs font-medium transition-colors
                  ${
                    isActive
                      ? 'bg-paper-200/80 text-ink-950 font-semibold border border-[#D5D2C7]'
                      : 'text-ink-600 hover:bg-paper-100 hover:text-ink-900 border border-transparent'
                  }
                  ${isCollapsedDesktop ? 'md:justify-center md:px-0' : ''}
                `}
                title={`${item.label} ${item.badge ? `(${item.badge})` : ''} — ${item.description}`}
              >
                <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-ink-900' : 'text-ink-500'}`} />
                {(!isCollapsedDesktop || isOpenMobile) && (
                  <div className="flex-1 flex items-center justify-between min-w-0">
                    <span className="truncate">{item.label}</span>
                    {item.badge && (
                      <span className="text-[9px] font-mono px-1 py-0.2 rounded bg-paper-100 text-ink-400 border border-[#E5E3D8]">
                        {item.badge}
                      </span>
                    )}
                  </div>
                )}
              </button>
            );
          })}
        </div>

        {/* Desktop Collapse Toggle Footer */}
        <div className="hidden md:flex p-2 border-t border-paper-200 justify-end">
          <button
            type="button"
            onClick={onToggleCollapseDesktop}
            className="w-full flex items-center justify-center p-1.5 text-xs font-mono text-ink-500 hover:bg-paper-100 hover:text-ink-800 rounded transition-colors"
            title={isCollapsedDesktop ? 'Expand Sidebar' : 'Collapse Sidebar'}
            aria-label={isCollapsedDesktop ? 'Expand Sidebar' : 'Collapse Sidebar'}
          >
            {isCollapsedDesktop ? (
              <ChevronRight className="w-4 h-4" />
            ) : (
              <div className="flex items-center gap-2 w-full px-1">
                <ChevronLeft className="w-4 h-4" />
                <span className="text-[11px] font-sans">Collapse</span>
              </div>
            )}
          </button>
        </div>
      </aside>
    </>
  );
};
