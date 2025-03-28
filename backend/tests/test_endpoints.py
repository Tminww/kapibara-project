import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app  # Импортируйте ваше FastAPI приложение из main.py


@pytest.mark.anyio
async def test_get_subjects():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/subjects")
    assert (
        response.status_code == 200
    ), f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    # Проверяем, что у первого элемента есть ключи: id, name, regions
    assert all(key in data["data"][0] for key in ["id", "name", "regions"])


@pytest.mark.anyio
async def test_get_subjects_regions():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/subjects/regions")
    assert (
        response.status_code == 200
    ), f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    # Проверяем, что у первого элемента есть ключи: id, name, regions
    assert all(key in data["data"][0] for key in ["id", "name"])
