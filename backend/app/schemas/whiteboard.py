from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field


class PhysicsVectorElement(BaseModel):
    id: str
    type: Literal["vector"]
    origin: str
    direction_deg: float
    magnitude: str
    label: str
    semantic_role: Literal[
        "real_force",
        "pseudo_force",
        "contact_force",
        "friction_force",
        "velocity",
        "acceleration",
    ]
    color: Optional[str] = None

    model_config = ConfigDict(extra="allow")


class PhysicsPolygonElement(BaseModel):
    id: str
    type: Literal["polygon"]
    points: List[List[float]]
    label: Optional[str] = None

    model_config = ConfigDict(extra="allow")


class Position2D(BaseModel):
    x: float
    y: float


class PhysicsRigidBodyElement(BaseModel):
    id: str
    type: Literal["rigid_body"]
    position: Position2D
    mass: float
    label: Optional[str] = None

    model_config = ConfigDict(extra="allow")


class DiagramNodeContent(BaseModel):
    canvas_type: Literal["PHYSICS_2D", "MATH_COORDINATE", "CHEM_STRUCTURE"]
    title: Optional[str] = None
    purpose: Optional[str] = None
    elements: List[Dict[str, Any]] = Field(default_factory=list)

    model_config = ConfigDict(extra="allow")


class WhiteboardStateCreate(BaseModel):
    id: Optional[str] = None
    explanation_document_id: str
    state_json: Dict[str, Any]
    version: int = 1


class WhiteboardStateResponse(BaseModel):
    id: str
    explanation_document_id: str
    state_json: Dict[str, Any]
    version: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
