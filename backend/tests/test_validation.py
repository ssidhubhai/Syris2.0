import pytest
from backend.app.ai.validation import SemanticValidationException, SemanticValidator
from backend.app.schemas.explanation import (
    ExplanationDocumentSchema,
    ExplanationNodeSchema,
    RelationshipSchema,
)


def _build_valid_doc() -> ExplanationDocumentSchema:
    return ExplanationDocumentSchema(
        document_id="doc-test-001",
        session_id="sess-test-001",
        title="Centripetal Acceleration",
        intent="definition",
        subject="physics",
        language="english",
        nodes=[
            ExplanationNodeSchema(
                id="node-head-1",
                type="heading",
                content={"text": "Centripetal Acceleration", "level": 1},
            ),
            ExplanationNodeSchema(
                id="node-def-1",
                type="definition",
                content={"title": "Definition of $a_c$", "latex": "a_c = \\frac{v^2}{r}"},
            ),
            ExplanationNodeSchema(
                id="node-eq-1",
                type="equation",
                content={"id_tag": "Eq. (1)", "label": "Angular Form", "latex": "a_c = \\omega^2 r"},
            ),
        ],
        relationships=[
            RelationshipSchema(
                from_node="node-def-1",
                to_node="node-eq-1",
                type="transforms_into",
            )
        ],
    )


def test_validation_passes_valid_document():
    doc = _build_valid_doc()
    # Should not raise
    SemanticValidator.validate(doc)


def test_validation_rejects_empty_nodes():
    doc = _build_valid_doc()
    doc.nodes = []
    with pytest.raises(SemanticValidationException, match="at least one node"):
        SemanticValidator.validate(doc)


def test_validation_rejects_duplicate_node_ids():
    doc = _build_valid_doc()
    doc.nodes.append(
        ExplanationNodeSchema(
            id="node-def-1",  # duplicate
            type="text",
            content={"markdown": "Duplicate node id"},
        )
    )
    with pytest.raises(SemanticValidationException, match="Duplicate node ID detected"):
        SemanticValidator.validate(doc)


def test_validation_rejects_dangling_from_relationship():
    doc = _build_valid_doc()
    doc.relationships.append(
        RelationshipSchema(
            from_node="node-ghost-404",  # does not exist
            to_node="node-eq-1",
            type="derives_from",
        )
    )
    with pytest.raises(SemanticValidationException, match="dangling reference"):
        SemanticValidator.validate(doc)


def test_validation_rejects_dangling_to_relationship():
    doc = _build_valid_doc()
    doc.relationships.append(
        RelationshipSchema(
            from_node="node-def-1",
            to_node="node-ghost-404",  # does not exist
            type="derives_from",
        )
    )
    with pytest.raises(SemanticValidationException, match="dangling reference"):
        SemanticValidator.validate(doc)


def test_validation_rejects_self_loop_relationship():
    doc = _build_valid_doc()
    doc.relationships.append(
        RelationshipSchema(
            from_node="node-def-1",
            to_node="node-def-1",  # self loop
            type="uses",
        )
    )
    with pytest.raises(SemanticValidationException, match="Self-referencing relationship"):
        SemanticValidator.validate(doc)


def test_validation_rejects_empty_equation_latex():
    doc = _build_valid_doc()
    doc.nodes[2].content = {"latex": ""}
    with pytest.raises(SemanticValidationException, match="non-empty 'latex'"):
        SemanticValidator.validate(doc)


def test_validation_rejects_empty_heading_text():
    doc = _build_valid_doc()
    doc.nodes[0].content = {"text": "  "}
    with pytest.raises(SemanticValidationException, match="non-empty 'text'"):
        SemanticValidator.validate(doc)
