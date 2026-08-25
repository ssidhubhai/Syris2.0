import { useState, useCallback } from 'react';

export function usePaperZoom() {
  const [zoomScale, setZoomScale] = useState<number>(1.0);

  const zoomIn = useCallback(() => {
    setZoomScale((prev) => Math.min(1.25, parseFloat((prev + 0.05).toFixed(2))));
  }, []);

  const zoomOut = useCallback(() => {
    setZoomScale((prev) => Math.max(0.8, parseFloat((prev - 0.05).toFixed(2))));
  }, []);

  const resetZoom = useCallback(() => {
    setZoomScale(1.0);
  }, []);

  return {
    zoomScale,
    zoomIn,
    zoomOut,
    resetZoom,
  };
}
