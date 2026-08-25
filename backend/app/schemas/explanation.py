from datetime import datetime
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field

NodeType = Literal[
    "heading",
    "text",
    "equation",
    "derivation_step",
    "diagram",
    "graph",
    "table",
    "comparison",
    "annotation",
    "callout",
    "definition",
    "assumption",
    "conclusion",
    "example",
    "checkpoint",
    "interactive_visual",
]

RelationshipType = Literal[
    "derives_from",
    "uses",
    "substitutes_into",
    "explains",
    "causes",
    "contrasts_with",
    "depends_on",
    "follows_from",
    "defines",
    "references",
    "highlights",
    "transforms_into",
]

NodeImportance = Literal["critical", "supporting", "note"]
LayoutPreference = Literal["full_width", "split_left", "split_right", "sticky_context", "auto"]


class ExplanationNodeSchema(BaseModel):
    id: str
    type: NodeType
    content: Any
    importance: Optional[NodeImportance] = "supporting"
    layout_preference: Optional[LayoutPreference] = "auto"

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class RelationshipSchema(BaseModel):
    from_node: str = Field(alias="from")
    to_node: str = Field(alias="to")
    type: RelationshipType
    label: Optional[str] = None

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class LayoutHintsSchema(BaseModel):
    recommended_layout: Optional[str] = None
    primary_channel_nodes: Optional[List[str]] = None
    context_channel_nodes: Optional[List[str]] = None
    sticky_header_nodes: Optional[List[str]] = None

    model_config = ConfigDict(extra="allow")


class ValidationMetadataSchema(BaseModel):
    math_verified: bool = False
    domain_verified: bool = False
    verifier_used: str = "not_run"
    flagged_issues: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="allow")


class SourceMetadataSchema(BaseModel):
    provider: str = "internal"
    model: str = "canonical_mock"
    generation_time_ms: int = 0

    model_config = ConfigDict(extra="allow")


class ExplanationDocumentSchema(BaseModel):
    document_id: str
    session_id: str
    title: str
    intent: str
    subject: Literal["physics", "chemistry", "mathematics", "general"] = "physics"
    language: str = "hinglish"
    nodes: List[ExplanationNodeSchema]
    relationships: List[RelationshipSchema] = Field(default_factory=list)
    layout_hints: Optional[LayoutHintsSchema] = None
    validation: ValidationMetadataSchema = Field(default_factory=ValidationMetadataSchema)
    source_metadata: SourceMetadataSchema = Field(default_factory=SourceMetadataSchema)

    model_config = ConfigDict(extra="allow", populate_by_name=True)




class ExplanationDocumentCreate(BaseModel):
    document: ExplanationDocumentSchema
    version: int = 1


class ExplanationDocumentResponse(BaseModel):
    id: str
    session_id: str
    title: str
    subject: str
    intent: str
    version: int
    document_json: Dict[str, Any]
    validation_json: Dict[str, Any]
    provider_metadata: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
