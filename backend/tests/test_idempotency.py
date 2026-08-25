import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_idempotency_replay_same_payload(client: AsyncClient):
    payload = {"title": "Idempotent Session", "subject": "mathematics"}
    headers = {"X-Idempotency-Key": "idem-key-001"}

    # First request
    resp1 = await client.post("/api/v1/sessions", json=payload, headers=headers)
    assert resp1.status_code == 201
    data1 = resp1.json()

    # Second request with identical key & payload
    resp2 = await client.post("/api/v1/sessions", json=payload, headers=headers)
    assert resp2.status_code == 201
    assert resp2.headers.get("X-Cache-Lookup") == "HIT"
    data2 = resp2.json()
    assert data1["id"] == data2["id"]

    # Verify no duplicate session was created
    list_resp = await client.get("/api/v1/sessions")
    sessions = [s for s in list_resp.json() if s["title"] == "Idempotent Session"]
    assert len(sessions) == 1


@pytest.mark.asyncio
async def test_idempotency_conflict_different_payload(client: AsyncClient):
    payload1 = {"title": "Original Session", "subject": "physics"}
    payload2 = {"title": "Conflicting Session", "subject": "chemistry"}
    headers = {"X-Idempotency-Key": "idem-conflict-key"}

    resp1 = await client.post("/api/v1/sessions", json=payload1, headers=headers)
    assert resp1.status_code == 201

    resp2 = await client.post("/api/v1/sessions", json=payload2, headers=headers)
    assert resp2.status_code == 409
    error_data = resp2.json()
    assert error_data["error"]["code"] == "IDEMPOTENCY_CONFLICT"


@pytest.mark.asyncio
async def test_message_idempotency(client: AsyncClient):
    sess_resp = await client.post("/api/v1/sessions", json={"title": "Message Idem Test"})
    session_id = sess_resp.json()["id"]

    msg_payload = {"role": "user", "content": "Question with idempotency"}
    headers = {"X-Idempotency-Key": "idem-msg-001"}

    resp1 = await client.post(
        f"/api/v1/sessions/{session_id}/messages",
        json=msg_payload,
        headers=headers,
    )
    assert resp1.status_code == 201
    msg1 = resp1.json()

    resp2 = await client.post(
        f"/api/v1/sessions/{session_id}/messages",
        json=msg_payload,
        headers=headers,
    )
    assert resp2.status_code == 201
    assert resp2.headers.get("X-Cache-Lookup") == "HIT"
    msg2 = resp2.json()
    assert msg1["id"] == msg2["id"]

    # Verify only 1 message in session
    list_resp = await client.get(f"/api/v1/sessions/{session_id}/messages")
    assert len(list_resp.json()) == 1
