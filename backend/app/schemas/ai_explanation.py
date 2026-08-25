"""
Dedicated AI Generation Schemas for Google Gemini Structured Output.

The Gemini Developer API enforces strict OpenAPI restrictions:
- No `additionalProperties: true`
- All properties and nested objects must have defined schemas
- `extra="ignore"` on all Pydantic models
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field
from backend.app.schemas.explanation import (
    NodeType,
    RelationshipType,
    NodeImportance,
    LayoutPreference,
)


class AINodeContentSchema(BaseModel):
    # Text / Heading
    text: Optional[str] = None
    level: Optional[int] = None
    markdown: Optional[str] = None
    description: Optional[str] = None
    subtitle: Optional[str] = None

    # Definition / Equation / Conclusion
    title: Optional[str] = None
    latex: Optional[str] = None
    equation: Optional[str] = None
    formula: Optional[str] = None
    expression: Optional[str] = None
    annotation: Optional[str] = None
    id_tag: Optional[str] = None
    label: Optional[str] = None
    highlight: Optional[bool] = None

    # Derivation step
    step_number: Optional[int] = None
    explanation: Optional[str] = None

    # Comparison
    left_title: Optional[str] = None
    left_points: Optional[List[str]] = None
    right_title: Optional[str] = None
    right_points: Optional[List[str]] = None

    # Callout
    callout_type: Optional[str] = None

    # Diagram semantic representation
    canvas_type: Optional[str] = None
    purpose: Optional[str] = None

    model_config = ConfigDict(extra="ignore")



class AIExplanationNodeSchema(BaseModel):
    id: str
    type: NodeType
    content: AINodeContentSchema
    importance: Optional[NodeImportance] = "supporting"
    layout_preference: Optional[LayoutPreference] = "auto"

    model_config = ConfigDict(extra="ignore", populate_by_name=True)


class AIRelationshipSchema(BaseModel):
    from_node: str = Field(alias="from")
    to_node: str = Field(alias="to")
    type: RelationshipType
    label: Optional[str] = None

    model_config = ConfigDict(extra="ignore", populate_by_name=True)


class AILayoutHintsSchema(BaseModel):
    recommended_layout: Optional[str] = None
    primary_channel_nodes: Optional[List[str]] = None
    context_channel_nodes: Optional[List[str]] = None
    sticky_header_nodes: Optional[List[str]] = None

    model_config = ConfigDict(extra="ignore")


class AIExplanationDocumentSchema(BaseModel):
    document_id: str
    session_id: str
    title: str
    intent: str
    subject: Literal["physics", "chemistry", "mathematics", "general"] = "physics"
    language: str = "hinglish"
    nodes: List[AIExplanationNodeSchema]
    relationships: List[AIRelationshipSchema] = Field(default_factory=list)
    layout_hints: Optional[AILayoutHintsSchema] = None

    model_config = ConfigDict(extra="ignore", populate_by_name=True)
