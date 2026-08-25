import pytest
from httpx import AsyncClient

CANONICAL_PHYSICS_DOC = {
    "document_id": "doc-test-incline-001",
    "session_id": "sess-test-001",
    "title": "Maximum Horizontal Acceleration of a Wedge with Friction",
    "intent": "problem_solution",
    "subject": "physics",
    "language": "hinglish",
    "nodes": [
        {
            "id": "node-head-1",
            "type": "heading",
            "content": {"text": "Finding Maximum Wedge Acceleration", "level": 1},
            "importance": "critical",
            "layout_preference": "full_width",
        },
        {
            "id": "node-diag-fbd",
            "type": "diagram",
            "content": {
                "canvas_type": "PHYSICS_2D",
                "title": "Free Body Diagram",
                "purpose": "Resolve forces",
                "elements": [
                    {
                        "id": "vec-mg",
                        "type": "vector",
                        "origin": "block.center",
                        "direction_deg": 270,
                        "magnitude": "m*g",
                        "label": "mg",
                        "semantic_role": "real_force",
                    }
                ],
            },
            "importance": "critical",
            "layout_preference": "split_right",
        },
        {
            "id": "node-eq-1",
            "type": "equation",
            "content": {"id_tag": "Eq. (1)", "latex": "N = m g \\cos\\theta + m a_0 \\sin\\theta"},
            "importance": "critical",
            "layout_preference": "split_left",
        },
    ],
    "relationships": [
        {
            "from": "node-diag-fbd",
            "to": "node-eq-1",
            "type": "explains",
            "label": "Normal force balance",
        }
    ],
    "layout_hints": {
        "recommended_layout": "hybrid_dual_channel",
        "primary_channel_nodes": ["node-eq-1"],
        "context_channel_nodes": ["node-diag-fbd"],
    },
    "validation": {
        "math_verified": True,
        "domain_verified": True,
        "verifier_used": "sympy_engine",
        "flagged_issues": [],
    },
    "source_metadata": {
        "provider": "canonical_mock",
        "model": "handcrafted_v1",
        "generation_time_ms": 120,
    },
}


@pytest.mark.asyncio
async def test_create_and_get_explanation(client: AsyncClient):
    sess_resp = await client.post("/api/v1/sessions", json={"id": "sess-test-001", "title": "Physics Session"})
    assert sess_resp.status_code == 201

    create_resp = await client.post(
        "/api/v1/sessions/sess-test-001/explanations",
        json=CANONICAL_PHYSICS_DOC,
    )
    assert create_resp.status_code == 201
    doc_data = create_resp.json()
    assert doc_data["id"] == "doc-test-incline-001"
    assert doc_data["session_id"] == "sess-test-001"
    assert doc_data["document_json"]["title"] == "Maximum Horizontal Acceleration of a Wedge with Friction"

    # Fetch latest
    latest_resp = await client.get("/api/v1/sessions/sess-test-001/explanations/latest")
    assert latest_resp.status_code == 200
    latest_data = latest_resp.json()
    assert latest_data["id"] == "doc-test-incline-001"
    assert len(latest_data["document_json"]["nodes"]) == 3
    assert len(latest_data["document_json"]["relationships"]) == 1

    # Check session detail reconstruction includes latest explanation and whiteboard state
    detail_resp = await client.get("/api/v1/sessions/sess-test-001")
    assert detail_resp.status_code == 200
    detail_data = detail_resp.json()
    assert detail_data["latest_explanation"] is not None
    assert detail_data["latest_explanation"]["id"] == "doc-test-incline-001"
    assert detail_data["latest_whiteboard"] is not None
    assert detail_data["latest_whiteboard"]["state_json"]["canvas_type"] == "PHYSICS_2D"


@pytest.mark.asyncio
async def test_reject_malformed_explanation(client: AsyncClient):
    sess_resp = await client.post("/api/v1/sessions", json={"title": "Invalid Test Session"})
    session_id = sess_resp.json()["id"]

    # Missing required nodes array
    invalid_doc = {
        "document_id": "doc-invalid-1",
        "session_id": session_id,
        "title": "Invalid Document",
        "intent": "problem_solution",
        "subject": "physics",
        # missing nodes
    }
    resp = await client.post(f"/api/v1/sessions/{session_id}/explanations", json=invalid_doc)
    assert resp.status_code == 422
    data = resp.json()
    assert data["error"]["code"] == "INVALID_PAYLOAD"


@pytest.mark.asyncio
async def test_create_explanation_for_missing_session(client: AsyncClient):
    resp = await client.post(
        "/api/v1/sessions/missing-sess/explanations",
        json=CANONICAL_PHYSICS_DOC,
    )
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "SESSION_NOT_FOUND"
