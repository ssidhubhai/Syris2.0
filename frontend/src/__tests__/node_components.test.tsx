import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { HeadingNodeView } from '@/components/nodes/HeadingNodeView';
import { EquationNodeView } from '@/components/nodes/EquationNodeView';
import { DerivationStepView } from '@/components/nodes/DerivationStepView';
import { ComparisonNodeView } from '@/components/nodes/ComparisonNodeView';
import { CalloutNodeView } from '@/components/nodes/CalloutNodeView';

describe('Unboxed Semantic Paper Components', () => {
  it('should render HeadingNodeView with academic badge and title', () => {
    render(
      <HeadingNodeView
        content={{ text: 'Finding Maximum Acceleration', level: 1 }}
      />
    );
    expect(screen.getByText(/Finding Maximum Acceleration/i)).toBeInTheDocument();
  });

  it('should render EquationNodeView with tag badge', () => {
    render(
      <EquationNodeView
        content={{
          id_tag: 'Eq. (1)',
          label: 'Perpendicular Equilibrium',
          latex: 'N = mg \cos\theta',
        }}
      />
    );
    expect(screen.getByText('Eq. (1)')).toBeInTheDocument();
    expect(screen.getByText('Perpendicular Equilibrium')).toBeInTheDocument();
  });

  it('should render DerivationStepView with step badge and title', () => {
    render(
      <DerivationStepView
        content={{
          step_number: 1,
          title: 'Substitute Normal Force',
          explanation: 'Substituting equation into equilibrium',
          latex: 'ma_0 = mg + f_s',
        }}
      />
    );
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('Substitute Normal Force')).toBeInTheDocument();
  });

  it('should render ComparisonNodeView with left and right columns', () => {
    render(
      <ComparisonNodeView
        content={{
          title: 'SN1 vs SN2 Matrix',
          left_title: 'SN1 Pathway',
          left_points: ['First order kinetics'],
          right_title: 'SN2 Pathway',
          right_points: ['Second order kinetics'],
        }}
      />
    );
    expect(screen.getByText('SN1 vs SN2 Matrix')).toBeInTheDocument();
    expect(screen.getByText('SN1 Pathway')).toBeInTheDocument();
    expect(screen.getByText('SN2 Pathway')).toBeInTheDocument();
    expect(screen.getByText(/First order kinetics/i)).toBeInTheDocument();
    expect(screen.getByText(/Second order kinetics/i)).toBeInTheDocument();
  });

  it('should render CalloutNodeView with Kota Trap Alert', () => {
    render(
      <CalloutNodeView
        content={{
          callout_type: 'warning',
          title: 'Kota Trap Alert',
          markdown: 'Denominator boundary check warning',
        }}
      />
    );
    expect(screen.getByText('Kota Trap Alert')).toBeInTheDocument();
    expect(screen.getByText(/Denominator boundary check warning/i)).toBeInTheDocument();
  });
});
