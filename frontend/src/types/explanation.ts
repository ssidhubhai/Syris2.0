export type NodeType =
  | 'heading'
  | 'text'
  | 'equation'
  | 'derivation_step'
  | 'diagram'
  | 'graph'
  | 'table'
  | 'comparison'
  | 'annotation'
  | 'callout'
  | 'definition'
  | 'assumption'
  | 'conclusion'
  | 'example'
  | 'checkpoint'
  | 'interactive_visual';

export type RelationshipType =
  | 'derives_from'
  | 'uses'
  | 'substitutes_into'
  | 'explains'
  | 'causes'
  | 'contrasts_with'
  | 'depends_on'
  | 'follows_from'
  | 'defines'
  | 'references'
  | 'highlights'
  | 'transforms_into';

export type NodeImportance = 'critical' | 'supporting' | 'note';
export type LayoutPreference = 'full_width' | 'split_left' | 'split_right' | 'sticky_context' | 'auto';

export interface HeadingNodeContent {
  text: string;
  level: number;
}

export interface TextNodeContent {
  markdown: string;
}

export interface DefinitionNodeContent {
  title: string;
  latex?: string;
  annotation?: string;
}

export interface EquationNodeContent {
  id_tag?: string;
  label?: string;
  latex: string;
}

export interface DerivationStepContent {
  step_number: number;
  title: string;
  explanation: string;
  latex: string;
}

export interface ComparisonNodeContent {
  title: string;
  left_title: string;
  left_points: string[];
  right_title: string;
  right_points: string[];
}

export interface CalloutNodeContent {
  callout_type: 'warning' | 'tip' | 'info' | 'trap';
  title: string;
  markdown: string;
}

export interface ConclusionNodeContent {
  title: string;
  latex: string;
  highlight?: boolean;
}

export interface ExplanationNode<T = any> {
  id: string;
  type: NodeType;
  content: T;
  importance?: NodeImportance;
  layout_preference?: LayoutPreference;
}

export interface Relationship {
  from: string;
  to: string;
  type: RelationshipType;
  label?: string | null;
}

export interface LayoutHints {
  recommended_layout?: string | null;
  primary_channel_nodes?: string[] | null;
  context_channel_nodes?: string[] | null;
  sticky_header_nodes?: string[] | null;
}

export interface ValidationMetadata {
  math_verified: boolean;
  domain_verified: boolean;
  verifier_used: string;
  flagged_issues: string[];
}

export interface SourceMetadata {
  provider: string;
  model: string;
  generation_time_ms: number;
  prompt_version?: string;
}

export interface ExplanationDocument {
  document_id: string;
  session_id: string;
  title: string;
  intent: string;
  subject: 'physics' | 'chemistry' | 'mathematics';
  language: string;
  nodes: ExplanationNode[];
  relationships: Relationship[];
  layout_hints?: LayoutHints;
  validation: ValidationMetadata;
  source_metadata: SourceMetadata;
}
