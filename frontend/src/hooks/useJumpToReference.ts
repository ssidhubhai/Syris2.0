import { useState, useCallback } from 'react';

export function useJumpToReference() {
  const [targetNodeId, setTargetNodeId] = useState<string | null>(null);

  const jumpToNode = useCallback((nodeId: string) => {
    setTargetNodeId(nodeId);

    const element = document.getElementById(nodeId);
    if (element) {
      element.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      });
    }

    const timeout = setTimeout(() => {
      setTargetNodeId((current) => (current === nodeId ? null : current));
    }, 2500);

    return () => clearTimeout(timeout);
  }, []);

  return {
    targetNodeId,
    jumpToNode,
  };
}
