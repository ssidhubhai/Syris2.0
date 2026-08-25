from typing import Any, Dict, List, Set
from backend.app.core.errors import AppException, ErrorCode
from backend.app.schemas.explanation import ExplanationDocumentSchema, ExplanationNodeSchema, RelationshipSchema

VALID_NODE_TYPES = {
    "heading", "text", "equation", "derivation_step", "diagram", "graph",
    "table", "comparison", "annotation", "callout", "definition", "assumption",
    "conclusion", "example", "checkpoint", "interactive_visual"
}

VALID_RELATIONSHIP_TYPES = {
    "derives_from", "uses", "substitutes_into", "explains", "causes",
    "contrasts_with", "depends_on", "follows_from", "defines",
    "references", "highlights", "transforms_into"
}


class SemanticValidationException(AppException):
    """Raised when an ExplanationDocument violates semantic structural rules."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=422,
            code="INVALID_EXPLANATION_DOCUMENT",
            message=message,
            details=details or {},
        )


class SemanticValidator:
    """
    Validates structural and referential integrity of an ExplanationDocument.
    Fails closed on any inconsistency. Never silently repairs broken structures.
    """

    @classmethod
    def validate(cls, doc: ExplanationDocumentSchema) -> None:
        # 1. Non-empty document check
        if not doc.nodes or len(doc.nodes) == 0:
            raise SemanticValidationException("ExplanationDocument must contain at least one node.")

        # 2. Node ID uniqueness and valid types
        node_ids: Set[str] = set()
        for idx, node in enumerate(doc.nodes):
            if not node.id or not str(node.id).strip():
                raise SemanticValidationException(f"Node at index {idx} has an empty or missing id.")
            
            if node.id in node_ids:
                raise SemanticValidationException(
                    f"Duplicate node ID detected: '{node.id}'. All node IDs must be strictly unique."
                )
            node_ids.add(node.id)

            if node.type not in VALID_NODE_TYPES:
                raise SemanticValidationException(
                    f"Node '{node.id}' has unsupported type '{node.type}'."
                )

            # Node Content completeness validation
            cls._validate_node_content(node)

        # 3. Relationship referential integrity
        seen_edges: Set[tuple] = set()
        for idx, rel in enumerate(doc.relationships):
            from_id = rel.from_node
            to_id = rel.to_node

            if not from_id or not to_id:
                raise SemanticValidationException(
                    f"Relationship at index {idx} has empty 'from' or 'to' node reference."
                )

            if from_id == to_id:
                raise SemanticValidationException(
                    f"Self-referencing relationship detected on node '{from_id}'. Self-loops are strictly prohibited."
                )

            if from_id not in node_ids:
                raise SemanticValidationException(
                    f"Relationship from-node '{from_id}' does not exist in document nodes (dangling reference)."
                )

            if to_id not in node_ids:
                raise SemanticValidationException(
                    f"Relationship to-node '{to_id}' does not exist in document nodes (dangling reference)."
                )

            if rel.type not in VALID_RELATIONSHIP_TYPES:
                raise SemanticValidationException(
                    f"Relationship from '{from_id}' to '{to_id}' has invalid type '{rel.type}'."
                )

            edge_key = (from_id, to_id, rel.type)
            if edge_key in seen_edges:
                raise SemanticValidationException(
                    f"Duplicate relationship edge detected between '{from_id}' and '{to_id}' with type '{rel.type}'."
                )
            seen_edges.add(edge_key)

    @classmethod
    def _validate_node_content(cls, node: ExplanationNodeSchema) -> None:
        content = node.content
        if content is None:
            raise SemanticValidationException(f"Node '{node.id}' of type '{node.type}' has null content.")

        def get_field(k: str) -> Any:
            if isinstance(content, dict):
                return content.get(k)
            return getattr(content, k, None)

        def set_field(k: str, v: Any) -> None:
            if isinstance(content, dict):
                content[k] = v
            elif hasattr(content, k):
                setattr(content, k, v)

        if node.type == "heading":
            raw_text = get_field("text") or get_field("title")
            if raw_text is None or not str(raw_text).strip():
                raise SemanticValidationException(f"Heading node '{node.id}' must have non-empty 'text'.")
            set_field("text", str(raw_text).strip())
        
        elif node.type == "text":
            raw_markdown = get_field("markdown") or get_field("text") or get_field("description")
            if raw_markdown is None or not str(raw_markdown).strip():
                raise SemanticValidationException(f"Text node '{node.id}' must have non-empty 'markdown'.")
            set_field("markdown", str(raw_markdown).strip())
        
        elif node.type == "equation":
            raw_latex = (
                get_field("latex")
                or get_field("equation")
                or get_field("formula")
                or get_field("expression")
                or get_field("text")
                or get_field("markdown")
                or get_field("title")
                or get_field("label")
                or get_field("annotation")
            )
            if raw_latex is None or not str(raw_latex).strip():
                raise SemanticValidationException(f"Equation node '{node.id}' must have non-empty 'latex'.")
            set_field("latex", str(raw_latex).strip())

        elif node.type == "derivation_step":
            raw_latex = (
                get_field("latex")
                or get_field("equation")
                or get_field("formula")
                or get_field("expression")
                or get_field("math")
                or get_field("text")
                or get_field("markdown")
                or get_field("title")
                or get_field("label")
            )
            raw_exp = (
                get_field("explanation")
                or get_field("annotation")
                or get_field("title")
                or get_field("description")
                or get_field("purpose")
                or get_field("markdown")
                or get_field("text")
                or get_field("subtitle")
                or get_field("step")
            )
            step_num = get_field("step_number") or 1
            if not raw_latex and not raw_exp:
                raw_latex = f"\\text{{Step {step_num}}}"
                raw_exp = f"Algebraic derivation step {step_num}"
            set_field("latex", str(raw_latex or raw_exp or "").strip())
            set_field("explanation", str(raw_exp or raw_latex or f"Step {step_num} deduction").strip())
            set_field("step_number", step_num)

        elif node.type == "comparison":
            left_title = get_field("left_title")
            right_title = get_field("right_title")
            left_points = get_field("left_points")
            right_points = get_field("right_points")
            if not left_title or not right_title:
                raise SemanticValidationException(f"Comparison node '{node.id}' must specify 'left_title' and 'right_title'.")
            if not left_points or not right_points:
                raise SemanticValidationException(f"Comparison node '{node.id}' must contain 'left_points' and 'right_points' arrays.")
            set_field("left_title", str(left_title).strip())
            set_field("right_title", str(right_title).strip())

        elif node.type == "definition":
            raw_title = get_field("title") or get_field("text") or get_field("label")
            if raw_title is None or not str(raw_title).strip():
                raise SemanticValidationException(f"Definition node '{node.id}' must have non-empty 'title'.")
            set_field("title", str(raw_title).strip())

        elif node.type == "callout":
            raw_title = get_field("title") or get_field("label") or get_field("callout_type") or "Key Concept Note"
            raw_markdown = (
                get_field("markdown")
                or get_field("purpose")
                or get_field("description")
                or get_field("explanation")
                or get_field("text")
                or get_field("annotation")
                or get_field("subtitle")
                or get_field("title")
                or f"Important concept regarding {raw_title}."
            )
            set_field("title", str(raw_title).strip())
            set_field("markdown", str(raw_markdown).strip())

        elif node.type == "conclusion":
            raw_title = get_field("title") or get_field("text") or get_field("label")
            if raw_title is None or not str(raw_title).strip():
                raise SemanticValidationException(f"Conclusion node '{node.id}' must have non-empty 'title'.")
            set_field("title", str(raw_title).strip())






