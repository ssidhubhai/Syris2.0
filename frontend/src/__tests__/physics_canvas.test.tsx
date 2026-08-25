import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { PhysicsCanvas2D } from '@/components/whiteboard/PhysicsCanvas2D';

describe('PhysicsCanvas2D Seamless Blackboard Component', () => {
  it('should render SVG canvas with Free Body Diagram and compact chips', () => {
    render(
      <PhysicsCanvas2D
        content={{
          canvas_type: 'PHYSICS_2D',
          title: 'Free Body Diagram',
          purpose: 'Resolve force vectors',
          elements: [],
        }}
      />
    );
    expect(screen.getByTestId('physics-canvas-2d')).toBeInTheDocument();
    expect(screen.getByText(/Free Body Diagram/i)).toBeInTheDocument();
    expect(screen.getByText('Gravity')).toBeInTheDocument();
    expect(screen.getByText('Pseudo Force')).toBeInTheDocument();
    expect(screen.getByText('Normal Force')).toBeInTheDocument();
    expect(screen.getByText('Friction')).toBeInTheDocument();
  });
});
