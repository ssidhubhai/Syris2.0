import pytest
from httpx import AsyncClient

# Exact canonical physics fixture matching frontend/src/fixtures/canonical_physics_fixture.ts
CANONICAL_PHYSICS_FIXTURE = {
    "document_id": "doc-p1-mechanics-incline-001",
    "session_id": "sess-contract-001",
    "title": "Maximum Horizontal Acceleration of a Wedge with Friction",
    "intent": "problem_solution",
    "subject": "physics",
    "language": "hinglish",
    "nodes": [
        {
            "id": "node-head-1",
            "type": "heading",
            "content": {
                "text": "Finding Maximum Wedge Acceleration ($a_{\\max}$) Before Upward Slip",
                "level": 1,
            },
            "importance": "critical",
            "layout_preference": "full_width",
        },
        {
            "id": "node-intro-1",
            "type": "text",
            "content": {
                "markdown": "Wedge ke accelerating frame (non-inertial frame) me block par ek pseudo-force $m a_0$ leftward act karega. Jab wedge rightwards acceleration $a_{\\max}$ se move karega, toh block ki tendency incline ke along **upward slip** karne ki hogi. Isliye static friction $f_s$ incline ke along **downward** act karega."
            },
            "importance": "supporting",
            "layout_preference": "full_width",
        },
        {
            "id": "node-sticky-law",
            "type": "definition",
            "content": {
                "title": "Governing Law: Limiting Static Friction",
                "latex": "f_s \\le f_{\\max} = \\mu_s N",
                "annotation": "Critical condition for impending upward slide: $f_s = \\mu_s N$",
            },
            "importance": "critical",
            "layout_preference": "sticky_context",
        },
        {
            "id": "node-diag-fbd",
            "type": "diagram",
            "content": {
                "canvas_type": "PHYSICS_2D",
                "title": "Free Body Diagram in Non-Inertial Frame of Wedge",
                "purpose": "Resolve real gravity, pseudo-force, normal force, and friction into components parallel and perpendicular to the incline.",
                "elements": [
                    {
                        "id": "elem-incline",
                        "type": "polygon",
                        "points": [[-5, -3], [5, -3], [5, 3]],
                        "label": "Wedge (Angle \\theta)",
                    },
                    {
                        "id": "elem-block",
                        "type": "rigid_body",
                        "position": {"x": 0.5, "y": 0.3},
                        "mass": 2.0,
                        "label": "Block (m)",
                    },
                    {
                        "id": "vec-mg",
                        "type": "vector",
                        "origin": "elem-block.center",
                        "direction_deg": 270,
                        "magnitude": "m*g",
                        "label": "m g (Gravity)",
                        "semantic_role": "real_force",
                    },
                    {
                        "id": "vec-pseudo",
                        "type": "vector",
                        "origin": "elem-block.center",
                        "direction_deg": 180,
                        "magnitude": "m*a_0",
                        "label": "m a_0 (Pseudo Force)",
                        "semantic_role": "pseudo_force",
                    },
                    {
                        "id": "vec-normal",
                        "type": "vector",
                        "origin": "elem-block.center",
                        "direction_deg": 120,
                        "magnitude": "N",
                        "label": "N (Normal Force)",
                        "semantic_role": "contact_force",
                    },
                    {
                        "id": "vec-friction",
                        "type": "vector",
                        "origin": "elem-block.surface_bottom",
                        "direction_deg": 210,
                        "magnitude": "f_s",
                        "label": "f_s (Static Friction)",
                        "semantic_role": "friction_force",
                    },
                ],
            },
            "importance": "critical",
            "layout_preference": "split_right",
        },
        {
            "id": "node-eq-normal",
            "type": "equation",
            "content": {
                "id_tag": "Eq. (1)",
                "label": "Perpendicular Equilibrium",
                "latex": "N = m g \\cos\\theta + m a_0 \\sin\\theta",
            },
            "importance": "critical",
            "layout_preference": "split_left",
        },
        {
            "id": "node-eq-tangential",
            "type": "equation",
            "content": {
                "id_tag": "Eq. (2)",
                "label": "Parallel Impending Slip Equilibrium",
                "latex": "m a_0 \\cos\\theta = m g \\sin\\theta + f_s",
            },
            "importance": "critical",
            "layout_preference": "split_left",
        },
        {
            "id": "node-deriv-substitute",
            "type": "derivation_step",
            "content": {
                "step_number": 1,
                "title": "Substitute Normal Force into Limiting Friction",
                "explanation": "Impending slip condition $f_s = \\mu_s N$ ko [Eq. (2)](ref://node-eq-tangential) me substitute karte hain, using $N$ from [Eq. (1)](ref://node-eq-normal):",
                "latex": "m a_0 \\cos\\theta = m g \\sin\\theta + \\mu_s (m g \\cos\\theta + m a_0 \\sin\\theta)",
            },
            "importance": "critical",
            "layout_preference": "split_left",
        },
        {
            "id": "node-deriv-isolate",
            "type": "derivation_step",
            "content": {
                "step_number": 2,
                "title": "Isolate Acceleration $a_0$",
                "explanation": "Dono sides se mass $m$ cancel karke $a_0$ terms ko left side me collect karte hain:",
                "latex": "a_0 (\\cos\\theta - \\mu_s \\sin\\theta) = g (\\sin\\theta + \\mu_s \\cos\\theta)",
            },
            "importance": "critical",
            "layout_preference": "split_left",
        },
        {
            "id": "node-conclusion-final",
            "type": "conclusion",
            "content": {
                "title": "Final Maximum Acceleration ($a_{\\max}$)",
                "latex": "a_{\\max} = g \\left( \\frac{\\sin\\theta + \\mu_s \\cos\\theta}{\\cos\\theta - \\mu_s \\sin\\theta} \\right) = g \\left( \\frac{\\tan\\theta + \\mu_s}{1 - \\mu_s \\tan\\theta} \\right)",
                "highlight": True,
            },
            "importance": "critical",
            "layout_preference": "full_width",
        },
        {
            "id": "node-callout-trap",
            "type": "callout",
            "content": {
                "callout_type": "warning",
                "title": "Kota Trap Alert: Boundary Condition Check",
                "markdown": "Agar $\\tan\\theta \\ge \\frac{1}{\\mu_s}$ ho jaye, toh denominator $\\le 0$ ho jayega. Iska physical significance hai ki wedge ko chahe infinite acceleration bhi de do, normal reaction itna increase ho jayega ki friction block ko slip hone hi nahi dega!",
            },
            "importance": "supporting",
            "layout_preference": "full_width",
        },
    ],
    "relationships": [
        {
            "from": "node-diag-fbd",
            "to": "node-eq-normal",
            "type": "explains",
            "label": "Perpendicular force balance",
        },
        {
            "from": "node-diag-fbd",
            "to": "node-eq-tangential",
            "type": "explains",
            "label": "Parallel force balance",
        },
        {
            "from": "node-sticky-law",
            "to": "node-deriv-substitute",
            "type": "uses",
            "label": "Limiting friction condition",
        },
        {
            "from": "node-eq-normal",
            "to": "node-deriv-substitute",
            "type": "substitutes_into",
            "label": "Substitute N",
        },
        {
            "from": "node-eq-tangential",
            "to": "node-deriv-substitute",
            "type": "substitutes_into",
            "label": "Substitute into equilibrium",
        },
        {
            "from": "node-deriv-substitute",
            "to": "node-deriv-isolate",
            "type": "derives_from",
            "label": "Algebraic simplification",
        },
        {
            "from": "node-deriv-isolate",
            "to": "node-conclusion-final",
            "type": "derives_from",
            "label": "Final expression",
        },
        {
            "from": "node-conclusion-final",
            "to": "node-callout-trap",
            "type": "highlights",
            "label": "Denominator singularity check",
        },
    ],
    "layout_hints": {
        "recommended_layout": "hybrid_dual_channel",
        "primary_channel_nodes": [
            "node-eq-normal",
            "node-eq-tangential",
            "node-deriv-substitute",
            "node-deriv-isolate",
        ],
        "context_channel_nodes": ["node-diag-fbd"],
        "sticky_header_nodes": ["node-sticky-law"],
    },
    "validation": {
        "math_verified": False,
        "domain_verified": False,
        "verifier_used": "not_run_static_fixture",
        "flagged_issues": [],
    },
    "source_metadata": {
        "provider": "static_mock_phase1",
        "model": "handcrafted_canonical_physics_v1",
        "generation_time_ms": 0,
    },
}


@pytest.mark.asyncio
async def test_canonical_fixture_roundtrip(client: AsyncClient):
    """
    Contract Roundtrip Test:
    1. Create session via POST /api/v1/sessions
    2. Add user message via POST /api/v1/sessions/{id}/messages
    3. Persist Canonical Physics ExplanationDocument via POST /api/v1/sessions/{id}/explanations
    4. Fetch full session via GET /api/v1/sessions/{id}
    5. Verify complete semantic equality and fidelity across all 10 nodes, 8 relationships,
       layout hints, FBD diagram elements, LaTeX equations, and markdown annotations.
    """
    # 1. Create Session
    session_res = await client.post(
        "/api/v1/sessions",
        json={
            "id": "sess-contract-001",
            "title": "Wedge Incline Contract Test Session",
            "subject": "physics",
        },
    )
    assert session_res.status_code == 201

    # 2. Append Message
    msg_res = await client.post(
        "/api/v1/sessions/sess-contract-001/messages",
        json={
            "role": "user",
            "content": "Why is friction acting downward on the wedge?",
        },
    )
    assert msg_res.status_code == 201

    # 3. Persist Explanation Document
    doc_res = await client.post(
        "/api/v1/sessions/sess-contract-001/explanations",
        json=CANONICAL_PHYSICS_FIXTURE,
    )
    assert doc_res.status_code == 201

    # 4. Reload Session Detail
    reload_res = await client.get("/api/v1/sessions/sess-contract-001")
    assert reload_res.status_code == 200
    session_data = reload_res.json()

    # 5. Assert Semantic Integrity
    assert session_data["id"] == "sess-contract-001"
    assert len(session_data["messages"]) == 1
    assert session_data["messages"][0]["content"] == "Why is friction acting downward on the wedge?"

    reloaded_doc = session_data["latest_explanation"]["document_json"]
    assert reloaded_doc["document_id"] == "doc-p1-mechanics-incline-001"
    assert reloaded_doc["title"] == CANONICAL_PHYSICS_FIXTURE["title"]
    assert reloaded_doc["subject"] == CANONICAL_PHYSICS_FIXTURE["subject"]
    assert len(reloaded_doc["nodes"]) == len(CANONICAL_PHYSICS_FIXTURE["nodes"]) == 10
    assert len(reloaded_doc["relationships"]) == len(CANONICAL_PHYSICS_FIXTURE["relationships"]) == 8

    # Compare node IDs and types in exact sequence
    for original_node, reloaded_node in zip(CANONICAL_PHYSICS_FIXTURE["nodes"], reloaded_doc["nodes"]):
        assert original_node["id"] == reloaded_node["id"]
        assert original_node["type"] == reloaded_node["type"]
        assert original_node["importance"] == reloaded_node["importance"]
        assert original_node["layout_preference"] == reloaded_node["layout_preference"]

    # Verify diagram node elements and vectors
    diag_node = next(n for n in reloaded_doc["nodes"] if n["id"] == "node-diag-fbd")
    assert diag_node["content"]["canvas_type"] == "PHYSICS_2D"
    assert len(diag_node["content"]["elements"]) == 6

    # Verify relationships match exactly
    for orig_rel, rel_rel in zip(CANONICAL_PHYSICS_FIXTURE["relationships"], reloaded_doc["relationships"]):
        assert orig_rel["from"] == rel_rel["from"]
        assert orig_rel["to"] == rel_rel["to"]
        assert orig_rel["type"] == rel_rel["type"]
        assert orig_rel["label"] == rel_rel["label"]

    # Verify layout hints
    assert reloaded_doc["layout_hints"]["recommended_layout"] == "hybrid_dual_channel"
    assert len(reloaded_doc["layout_hints"]["primary_channel_nodes"]) == 4
