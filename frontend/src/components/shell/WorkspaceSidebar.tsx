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
          fixed md:sticky top-0 md:top-[49px] bottom-0 z-50 md:z-30
          bg-white/95 md:bg-white/80 backdrop-blur-md border-r border-paper-300
          transition-all duration-200 ease-in-out flex flex-col justify-between
          ${isOpenMobile ? 'translate-x-0 w-64' : '-translate-x-full md:translate-x-0'}
          ${isCollapsedDesktop ? 'md:w-14' : 'md:w-56'}
          h-full md:h-[calc(100vh-49px)]
        `}
        aria-label="Workspace Navigation"
      >
        {/* Top Header (Mobile only close button) */}
        <div className="p-3 border-b border-paper-200 flex items-center justify-between md:hidden">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded bg-[#16202C] text-white flex items-center justify-center font-bold text-[10px] font-mono">
              SY
            </div>
            <span className="text-xs font-bold text-ink-900 font-mono">WORKSPACE MENU</span>
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
        <div className="flex-1 py-3 px-2 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentSection === item.id;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => handleNavClick(item.id)}
                className={`
                  w-full flex items-center gap-3 px-2.5 py-2 rounded-md text-xs font-medium transition-colors
                  ${
                    isActive
                      ? 'bg-sky-50 text-sky-900 font-semibold shadow-xs border border-sky-200/60'
                      : 'text-ink-700 hover:bg-paper-100 hover:text-ink-900'
                  }
                  ${isCollapsedDesktop ? 'md:justify-center md:px-0' : ''}
                `}
                title={`${item.label} ${item.badge ? `(${item.badge})` : ''} — ${item.description}`}
              >
                <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-sky-700' : 'text-ink-500'}`} />
                {(!isCollapsedDesktop || isOpenMobile) && (
                  <div className="flex-1 flex items-center justify-between min-w-0">
                    <span className="truncate">{item.label}</span>
                    {item.badge && (
                      <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-paper-200 text-ink-500 border border-paper-300 font-semibold">
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
