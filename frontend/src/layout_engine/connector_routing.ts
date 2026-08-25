export interface Point {
  x: number;
  y: number;
}

export interface ConnectorCurve {
  path: string;
  start: Point;
  end: Point;
  labelPosition: Point;
}

export function calculateBezierConnector(
  fromRect: DOMRect,
  toRect: DOMRect,
  containerRect: DOMRect
): ConnectorCurve {
  const fromRelative = {
    top: fromRect.top - containerRect.top,
    bottom: fromRect.bottom - containerRect.top,
    left: fromRect.left - containerRect.left,
    right: fromRect.right - containerRect.left,
    centerX: fromRect.left - containerRect.left + fromRect.width / 2,
    centerY: fromRect.top - containerRect.top + fromRect.height / 2,
  };

  const toRelative = {
    top: toRect.top - containerRect.top,
    bottom: toRect.bottom - containerRect.top,
    left: toRect.left - containerRect.left,
    right: toRect.right - containerRect.left,
    centerX: toRect.left - containerRect.left + toRect.width / 2,
    centerY: toRect.top - containerRect.top + toRect.height / 2,
  };

  const isSideBySide = Math.abs(fromRelative.centerX - toRelative.centerX) > 100;
  
  let start: Point;
  let end: Point;
  let cp1: Point;
  let cp2: Point;

  if (isSideBySide) {
    if (fromRelative.centerX < toRelative.centerX) {
      start = { x: fromRelative.right, y: fromRelative.centerY };
      end = { x: toRelative.left, y: toRelative.centerY };
      const dx = Math.abs(end.x - start.x) * 0.5;
      cp1 = { x: start.x + dx, y: start.y };
      cp2 = { x: end.x - dx, y: end.y };
    } else {
      start = { x: fromRelative.left, y: fromRelative.centerY };
      end = { x: toRelative.right, y: toRelative.centerY };
      const dx = Math.abs(start.x - end.x) * 0.5;
      cp1 = { x: start.x - dx, y: start.y };
      cp2 = { x: end.x + dx, y: end.y };
    }
  } else {
    if (fromRelative.centerY < toRelative.centerY) {
      start = { x: fromRelative.centerX, y: fromRelative.bottom };
      end = { x: toRelative.centerX, y: toRelative.top };
      const dy = Math.abs(end.y - start.y) * 0.5;
      cp1 = { x: start.x, y: start.y + dy };
      cp2 = { x: end.x, y: end.y - dy };
    } else {
      start = { x: fromRelative.centerX, y: fromRelative.top };
      end = { x: toRelative.centerX, y: toRelative.bottom };
      const dy = Math.abs(start.y - end.y) * 0.5;
      cp1 = { x: start.x, y: start.y - dy };
      cp2 = { x: end.x, y: end.y + dy };
    }
  }

  const path = `M ${start.x} ${start.y} C ${cp1.x} ${cp1.y}, ${cp2.x} ${cp2.y}, ${end.x} ${end.y}`;
  
  const labelPosition = {
    x: 0.125 * start.x + 0.375 * cp1.x + 0.375 * cp2.x + 0.125 * end.x,
    y: 0.125 * start.y + 0.375 * cp1.y + 0.375 * cp2.y + 0.125 * end.y,
  };

  return {
    path,
    start,
    end,
    labelPosition,
  };
}
