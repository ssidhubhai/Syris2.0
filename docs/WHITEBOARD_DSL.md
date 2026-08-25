# WHITEBOARD_DSL.md — Semantic Visual Language

## 1. Principle

AI outputs semantic drawing instructions; deterministic renderers calculate actual positions and render them.

## 2. V1 primitives

```text
point
line
arrow/vector
circle
arc
rectangle/rigid_body
axis
label
angle
charge
field_line
highlight
brace
connector
region
text_note
```

## 3. Transformations

```text
move
rotate
scale
highlight
fade
replace
show/hide
morph (only where deterministic)
```

## 4. Canvas document

```json
{
  "canvas_type": "PHYSICS_2D",
  "elements": [],
  "connections": [],
  "states": [],
  "viewport": {}
}
```

## 5. Example

```json
{
  "type":"draw_vector",
  "target":"block.center",
  "direction":"down",
  "magnitude":"m*g",
  "label":"mg",
  "semantic_role":"force"
}
```

The renderer decides final coordinates and styles.

## 6. Diagram selection

The Presentation Planner must be able to choose:
- no diagram;
- one diagram;
- sequence of diagrams;
- diagram + equation;
- interactive diagram.

This decision is contextual, not hard-coded.

## 7. Subject renderers

Physics renderer:
- FBD;
- vectors;
- axes;
- graphs;
- circuits;
- field lines.

Math renderer:
- graph;
- coordinate plane;
- 2D/3D geometry later;
- construction relationships.

Chemistry renderer:
- structures;
- bonds;
- reaction arrows;
- curved-arrow mechanism later;
- stereochemistry later.
