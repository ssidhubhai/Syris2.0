import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_request_id_propagation(client: AsyncClient):
    custom_req_id = "req-client-traced-12345"
    response = await client.get("/api/v1/health", headers={"X-Request-ID": custom_req_id})
    assert response.status_code == 200
    assert response.headers.get("X-Request-ID") == custom_req_id


@pytest.mark.asyncio
async def test_generated_request_id(client: AsyncClient):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    generated_id = response.headers.get("X-Request-ID")
    assert generated_id is not None
    assert generated_id.startswith("req-")


@pytest.mark.asyncio
async def test_error_response_contains_request_id(client: AsyncClient):
    custom_req_id = "req-err-traced-999"
    response = await client.get(
        "/api/v1/sessions/nonexistent-session",
        headers={"X-Request-ID": custom_req_id},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["request_id"] == custom_req_id
    assert "error" in data
    assert data["error"]["code"] == "SESSION_NOT_FOUND"
