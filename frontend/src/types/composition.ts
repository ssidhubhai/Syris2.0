import { ExplanationNode } from './explanation';

export type CompositionPattern =
  | 'DERIVATION_CENTRIC'
  | 'DIAGRAM_CENTRIC'
  | 'CONCEPT_CENTRIC'
  | 'COMPARISON'
  | 'SEQUENTIAL_TRANSFORMATION'
  | 'MIXED_EXPLANATION'
  | 'COMPACT_EXPLANATION';

export type CompositionArrangement =
  | 'vertical_flow'
  | 'horizontal_pair'
  | 'visual_with_explanation'
  | 'equation_with_annotation'
  | 'visual_sequence'
  | 'comparison_columns'
  | 'inline_reference'
  | 'grouped_cluster'
  | 'emphasis_block';

export interface CompositionGroup {
  id: string;
  node_ids: string[];
  arrangement: CompositionArrangement;
  semantic_role: 'primary' | 'supporting' | 'context' | 'marginalia' | 'synthesis';
  priority: number;
  layout_hint?: {
    split_ratio?: 'balanced' | 'visual_dominant' | 'derivation_dominant';
    visual_placement?: 'left' | 'right' | 'top' | 'inline';
    collapse_behavior?: 'stack' | 'wrap' | 'inline';
  };
  relationship_ids?: string[];
}

export interface CompositionPlan {
  pattern: CompositionPattern;
  headerGroup?: CompositionGroup;
  stickyContextGroup?: CompositionGroup;
  groups: CompositionGroup[];
  synthesisGroup?: CompositionGroup;
}
