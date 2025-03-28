import pytest
from httpx import ASGITransport, AsyncClient
from src.main import app

async def assert_successful_response(response, expected_keys):
    """Helper function to validate response structure."""
    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}: {response.text}"
    )
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    assert all(key in data["data"][0] for key in expected_keys)

@pytest.mark.anyio
async def test_get_subjects():
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        response = await ac.get("/api/subjects")
    await assert_successful_response(response, ["id", "name", "regions"])

@pytest.mark.anyio
async def test_get_subjects_regions():
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:    
        response = await ac.get("/api/subjects/regions")
    await assert_successful_response(response, ["id", "name"])
    
@pytest.mark.anyio
async def test_get_subjects_regions_by_district_name():
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:    
        response = await ac.get("/api/subjects/regions?districtName=ЦФО")
    await assert_successful_response(response, ["id", "name"])
    
@pytest.mark.anyio
async def test_get_subjects_regions_by_district_short_name():
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:    
        response = await ac.get("/api/subjects/regions?districtName=Центральный ФО")
    await assert_successful_response(response, ["id", "name"])
    
@pytest.mark.anyio
async def test_get_subjects_regions_by_district_full_name():
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:    
        response = await ac.get("/api/subjects/regions?districtName=Центральный Федеральный округ")
    await assert_successful_response(response, ["id", "name"])
    
@pytest.mark.anyio
async def test_get_subjects_regions_by_district_id():
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:    
        response = await ac.get("/api/subjects/regions?districtId=1")
    await assert_successful_response(response, ["id", "name"])
    
@pytest.mark.anyio
async def test_get_subjects_regions_by_district_id_and_district_name():
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:    
        response = await ac.get("/api/subjects/regions?districtId=1&districtName=ЦФО")
    assert response.status_code == 422, (
        f"Expected 422, got {response.status_code}: {response.text}"
    )
    
@pytest.mark.anyio
async def test_get_subjects_districts():
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:    
        response = await ac.get("/api/subjects/districts")
    await assert_successful_response(response, ["id", "name"])
    