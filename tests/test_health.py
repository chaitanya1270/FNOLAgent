import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint_is_reachable():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        resp = await client.get("/health")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"


@pytest.mark.asyncio
async def test_health_response_is_json():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        resp = await client.get("/health")
    assert resp.headers["content-type"].startswith("application/json")


@pytest.mark.asyncio
@pytest.mark.parametrize("expected_key", ["status", "version", "model"])
async def test_health_response_has_required_keys(expected_key):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        resp = await client.get("/health")
    assert expected_key in resp.json(), f"Key '{expected_key}' missing from health response"


@pytest.mark.asyncio
async def test_health_status_is_healthy():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        resp = await client.get("/health")
    assert resp.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_health_model_references_gpt():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        resp = await client.get("/health")
    assert "gpt" in resp.json()["model"].lower(), "Model name should reference GPT"


@pytest.mark.asyncio
async def test_health_version_is_string():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        resp = await client.get("/health")
    assert isinstance(resp.json()["version"], str)
