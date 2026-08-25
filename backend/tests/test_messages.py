import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_list_messages(client: AsyncClient):
    sess_resp = await client.post("/api/v1/sessions", json={"title": "Chat Session", "subject": "physics"})
    session_id = sess_resp.json()["id"]

    msg1_resp = await client.post(
        f"/api/v1/sessions/{session_id}/messages",
        json={
            "role": "user",
            "content": "Why is friction acting downward along the incline?",
        },
    )
    assert msg1_resp.status_code == 201
    msg1_data = msg1_resp.json()
    assert msg1_data["session_id"] == session_id
    assert msg1_data["role"] == "user"
    assert msg1_data["content"] == "Why is friction acting downward along the incline?"

    msg2_resp = await client.post(
        f"/api/v1/sessions/{session_id}/messages",
        json={
            "role": "assistant",
            "content": "Because the wedge is accelerating rightwards, causing impending upward slip.",
        },
    )
    assert msg2_resp.status_code == 201

    list_resp = await client.get(f"/api/v1/sessions/{session_id}/messages")
    assert list_resp.status_code == 200
    messages = list_resp.json()
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


@pytest.mark.asyncio
async def test_create_message_for_invalid_session(client: AsyncClient):
    resp = await client.post(
        "/api/v1/sessions/nonexistent-sess/messages",
        json={"role": "user", "content": "Hello"},
    )
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "SESSION_NOT_FOUND"


@pytest.mark.asyncio
async def test_message_with_attachments(client: AsyncClient):
    sess_resp = await client.post("/api/v1/sessions", json={"title": "Attachment Session"})
    session_id = sess_resp.json()["id"]

    resp = await client.post(
        f"/api/v1/sessions/{session_id}/messages",
        json={
            "role": "user",
            "content": "Check my diagram attempt.",
            "attachments": [
                {"type": "image", "uri": "https://storage.example.com/attempt1.png"}
            ],
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert len(data["attachments"]) == 1
    assert data["attachments"][0]["uri"] == "https://storage.example.com/attempt1.png"
