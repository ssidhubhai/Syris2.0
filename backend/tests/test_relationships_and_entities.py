import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.models.user import UserModel
from backend.app.db.models.session import SessionModel
from backend.app.db.models.problem import ProblemModel
from backend.app.db.models.attempt import AttemptModel
from backend.app.db.models.explanation import ExplanationDocumentModel
from backend.app.db.models.whiteboard import WhiteboardStateModel
from backend.app.db.models.model_request import ModelRequestModel
from backend.app.db.models.mistake import MistakeModel


@pytest.mark.asyncio
async def test_full_entity_relationships_and_cascade(db_session: AsyncSession):
    # 1. Create User
    user = UserModel(id="usr-test-1", preferences={"theme": "paper", "language": "hinglish"})
    db_session.add(user)
    await db_session.flush()

    # 2. Create Session linked to User
    session = SessionModel(
        id="sess-rel-001",
        user_id="usr-test-1",
        title="Relationship Integrity Test",
        subject="physics",
        current_state="active",
    )
    db_session.add(session)
    await db_session.flush()

    # 3. Create Problem
    problem = ProblemModel(
        id="prob-001",
        session_id="sess-rel-001",
        normalized_text="Find tension in the string.",
        subject="physics",
        problem_metadata={"chapter": "NLM"},
    )
    db_session.add(problem)
    await db_session.flush()

    # 4. Create Attempt
    attempt = AttemptModel(
        id="att-001",
        problem_id="prob-001",
        raw_input="T - mg = ma",
        normalized_input="T = m(g + a)",
        analysis={"is_correct": True},
    )
    db_session.add(attempt)
    await db_session.flush()

    # 5. Create ExplanationDocument
    explanation = ExplanationDocumentModel(
        id="doc-rel-001",
        session_id="sess-rel-001",
        title="Tension Derivation",
        subject="physics",
        intent="derivation",
        version=1,
        document_json={"document_id": "doc-rel-001", "nodes": []},
    )
    db_session.add(explanation)
    await db_session.flush()

    # 6. Create WhiteboardState
    wb_state = WhiteboardStateModel(
        id="wb-rel-001",
        explanation_document_id="doc-rel-001",
        state_json={"canvas_type": "PHYSICS_2D", "elements": []},
        version=1,
    )
    db_session.add(wb_state)
    await db_session.flush()

    # 7. Create Mistake Record
    mistake = MistakeModel(
        id="mis-001",
        session_id="sess-rel-001",
        concept="Sign convention for upward acceleration",
        category="conceptual",
        evidence={"student_formula": "T + mg = ma"},
    )
    db_session.add(mistake)
    await db_session.flush()

    # 8. Create ModelRequest Telemetry Record
    model_req = ModelRequestModel(
        id="req-sim-001",
        session_id="sess-rel-001",
        provider="simulated",
        model="sim-physics-v1",
        request_type="derivation_planning",
        latency_ms=85,
        token_usage={"input": 200, "output": 450},
        status="success",
    )
    db_session.add(model_req)
    await db_session.flush()

    # Verify all records exist
    res_prob = (await db_session.execute(select(ProblemModel).where(ProblemModel.id == "prob-001"))).scalar_one()
    assert res_prob.session_id == "sess-rel-001"

    res_att = (await db_session.execute(select(AttemptModel).where(AttemptModel.id == "att-001"))).scalar_one()
    assert res_att.problem_id == "prob-001"

    res_mistake = (await db_session.execute(select(MistakeModel).where(MistakeModel.id == "mis-001"))).scalar_one()
    assert res_mistake.concept == "Sign convention for upward acceleration"

    res_req = (await db_session.execute(select(ModelRequestModel).where(ModelRequestModel.id == "req-sim-001"))).scalar_one()
    assert res_req.status == "success"

    # 9. Test Cascade Delete on Session
    await db_session.delete(session)
    await db_session.flush()

    # Verify child records (problems, attempts, explanations, whiteboard, mistakes) are deleted via cascade
    assert (await db_session.execute(select(ProblemModel).where(ProblemModel.id == "prob-001"))).scalar_one_or_none() is None
    assert (await db_session.execute(select(AttemptModel).where(AttemptModel.id == "att-001"))).scalar_one_or_none() is None
    assert (await db_session.execute(select(ExplanationDocumentModel).where(ExplanationDocumentModel.id == "doc-rel-001"))).scalar_one_or_none() is None
    assert (await db_session.execute(select(WhiteboardStateModel).where(WhiteboardStateModel.id == "wb-rel-001"))).scalar_one_or_none() is None
    assert (await db_session.execute(select(MistakeModel).where(MistakeModel.id == "mis-001"))).scalar_one_or_none() is None

    # Model request should have session_id set to null (ondelete=SET NULL)
    reloaded_req = (await db_session.execute(select(ModelRequestModel).where(ModelRequestModel.id == "req-sim-001"))).scalar_one()
    assert reloaded_req.session_id is None
