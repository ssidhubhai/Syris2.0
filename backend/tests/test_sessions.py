import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_session(client: AsyncClient):
    payload = {
        "title": "Mechanics Practice Session",
        "subject": "physics",
    }
    response = await client.post("/api/v1/sessions", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Mechanics Practice Session"
    assert data["subject"] == "physics"
    assert data["current_state"] == "active"
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_session_with_initial_problem(client: AsyncClient):
    payload = {
        "title": "Wedge Incline Session",
        "subject": "physics",
        "initial_problem": {
            "normalized_text": "A block of mass m is placed on a wedge of angle theta.",
            "subject": "physics",
            "problem_metadata": {"difficulty": "JEE_ADVANCED"},
        },
    }
    create_resp = await client.post("/api/v1/sessions", json=payload)
    assert create_resp.status_code == 201
    session_id = create_resp.json()["id"]

    detail_resp = await client.get(f"/api/v1/sessions/{session_id}")
    assert detail_resp.status_code == 200
    detail_data = detail_resp.json()
    assert len(detail_data["problems"]) == 1
    assert detail_data["problems"][0]["normalized_text"] == "A block of mass m is placed on a wedge of angle theta."


@pytest.mark.asyncio
async def test_get_session_not_found(client: AsyncClient):
    response = await client.get("/api/v1/sessions/nonexistent-session-id")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "SESSION_NOT_FOUND"
    assert "request_id" in data


@pytest.mark.asyncio
async def test_update_session(client: AsyncClient):
    create_resp = await client.post("/api/v1/sessions", json={"title": "Original Title", "subject": "physics"})
    session_id = create_resp.json()["id"]

    update_payload = {"title": "Updated Title", "current_state": "closed"}
    patch_resp = await client.patch(f"/api/v1/sessions/{session_id}", json=update_payload)
    assert patch_resp.status_code == 200
    assert patch_resp.json()["title"] == "Updated Title"
    assert patch_resp.json()["current_state"] == "closed"


@pytest.mark.asyncio
async def test_list_sessions(client: AsyncClient):
    await client.post("/api/v1/sessions", json={"title": "Session 1", "subject": "physics"})
    await client.post("/api/v1/sessions", json={"title": "Session 2", "subject": "chemistry"})

    list_resp = await client.get("/api/v1/sessions")
    assert list_resp.status_code == 200
    sessions = list_resp.json()
    assert len(sessions) >= 2
