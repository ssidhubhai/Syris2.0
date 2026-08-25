export interface PhysicsVectorElement {
  id: string;
  type: 'vector';
  origin: string;
  direction_deg: number;
  magnitude: string;
  label: string;
  semantic_role: 'real_force' | 'pseudo_force' | 'contact_force' | 'friction_force' | 'velocity' | 'acceleration';
  color?: string;
}

export interface PhysicsPolygonElement {
  id: string;
  type: 'polygon';
  points: [number, number][];
  label?: string;
}

export interface PhysicsRigidBodyElement {
  id: string;
  type: 'rigid_body';
  position: { x: number; y: number };
  mass: number;
  label?: string;
}

export type Physics2DElement = PhysicsVectorElement | PhysicsPolygonElement | PhysicsRigidBodyElement | any;

export interface DiagramNodeContent {
  canvas_type: 'PHYSICS_2D' | 'MATH_COORDINATE' | 'CHEM_STRUCTURE';
  title?: string;
  purpose?: string;
  elements: Physics2DElement[];
}
