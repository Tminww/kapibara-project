import pytest
from jsonschema import validate

from httpx import ASGITransport, AsyncClient
from src.main import app
from .schemas import (
    subjects_schema,
    subjects_regions_schema,
    subjects_districts_schema,
)


@pytest.fixture(scope="module")
async def client():
    """Фикстура клиента для всех тестов класса"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as test_client:
        yield test_client


async def assert_successful_response(response, expected_keys):
    """Вспомогательный метод для проверки успешных ответов"""
    assert (
        response.status_code == 200
    ), f"Expected 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert "data" in data, "Missing 'data' field in response"
    assert isinstance(data["data"], list), "'data' should be a list"
    assert len(data["data"]) > 0, "Empty data list in response"

    first_item = data["data"][0]
    missing_keys = [key for key in expected_keys if key not in first_item]
    assert (
        not missing_keys
    ), f"Missing keys in response: {missing_keys}. Response: {first_item}"


async def assert_json_structure(response, schema: dict):
    """Валидация по JSON Schema"""
    validate(instance=response.json(), schema=schema)


async def assert_status_code(response, expected_status):
    assert (
        response.status_code == expected_status
    ), f"Expected {expected_status}, got {response.status_code}. Response: {response.text}"


@pytest.mark.asyncio(loop_scope="module")
class TestSubjectsEndpoints:

    async def test_subjects_valid(self, client: AsyncClient):
        response = await client.get("/api/subjects")
        await assert_successful_response(response, ["id", "name"])
        await assert_status_code(response, 200)
        await assert_json_structure(response, subjects_schema)

    @pytest.mark.parametrize(
        "params, expected_keys",
        [
            ({"districtName": "ЦФО"}, ["id", "name"]),
            ({"districtName": "Центральный ФО"}, ["id", "name"]),
            ({"districtName": "Центральный Федеральный округ"}, ["id", "name"]),
            ({"districtId": "1"}, ["id", "name"]),
        ],
    )
    async def test_subjects_regions_valid(
        self, client: AsyncClient, params: dict[str, str], expected_keys: list[str]
    ):
        """Параметризованный тест валидных фильтров"""
        response = await client.get("/api/subjects/regions", params=params)
        await assert_status_code(response, 200)
        await assert_json_structure(response, subjects_regions_schema)

    @pytest.mark.parametrize(
        "params, expected_status",
        [
            ({"districtId": "1", "districtName": "ЦФО"}, 422),
            ({"districtName": "invalid_name"}, 400),
            ({"districtId": "invalid_id"}, 422),
        ],
    )
    async def test_subjects_regions_invalid(
        self, client: AsyncClient, params: dict[str, str], expected_status: int
    ):
        """Тестирование невалидных параметров фильтрации"""
        response = await client.get("/api/subjects/regions", params=params)
        await assert_status_code(response, expected_status)
        # await assert_json_structure(response, subjects_schema)

    async def test_subjects_districts_valid(self, client: AsyncClient):
        response = await client.get("/api/subjects/districts")
        await assert_status_code(response, 200)
        await assert_json_structure(response, subjects_districts_schema)


@pytest.mark.asyncio(loop_scope="module")
class TestStatisticsEndpoints:

    @pytest.mark.parametrize(
        "params",
        [
            {},
            {"ids": "440,441"},
            {"startDate": "20.10.2020"},
            {"endDate": "20.10.2020"},
            {"startDate": "20.10.2020", "endDate": "20.10.2025"},
            {"startDate": "20.10.2020", "ids": "440,441"},
        ],
    )
    async def test_statistics_valid(self, client: AsyncClient, params: dict[str, str]):
        response = await client.get("/api/statistics", params=params)
        await assert_status_code(response, 200)
