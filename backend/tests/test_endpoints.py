import re
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
    ) as client:
        yield client


async def assert_json_structure(response, schema: dict):
    """Валидация по JSON Schema"""
    validate(instance=response.json(), schema=schema)


async def assert_status_code(response, expected_status):
    assert (
        response.status_code == expected_status
    ), f"Expected {expected_status}, got {response.status_code}. Response: {response.text}"


async def assert_date(response, params: dict):
    data: dict = response.json()
    if data.get("startDate") and params.get("startDate"):
        assert re.match(
            r"^\d{4}-\d{2}-\d{2}$", data["startDate"]
        ), f"startDate '{data['startDate']}' is not in YYYY-MM-DD format"
    if data.get("endDate") and params.get("endDate"):
        assert re.match(
            r"^\d{4}-\d{2}-\d{2}$", data["endDate"]
        ), f"endDate '{data['endDate']}' is not in YYYY-MM-DD format"


@pytest.mark.asyncio(loop_scope="module")
class TestSubjectsEndpoints:

    async def test_subjects_valid(self, client: AsyncClient):
        response = await client.get("/api/subjects")
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
        await assert_date(response, params)

    @pytest.mark.parametrize(
        "params",
        [
            {},  # Без дат и ids
            {"startDate": "2020-10-20", "endDate": "2025-03-31"},  # Только даты
            {"ids": "440,441"},  # Только ids
            {
                "startDate": "2020-10-20",
                "endDate": "2025-03-31",
                "ids": "440,441",
            },  # Даты и ids
        ],
    )
    async def test_statistics_districts_stat_valid(
        self, client: AsyncClient, params: dict[str, str]
    ):
        """Тест эндпоинта /statistics/districts с валидными параметрами"""
        response = await client.get("/api/statistics/districts", params=params)
        await assert_status_code(response, 200)
        await assert_date(response, params)

    @pytest.mark.parametrize(
        "dist_id, params",
        [
            (1, {}),  # Без дат и ids
            (1, {"startDate": "2020-10-20", "endDate": "2025-03-31"}),  # Только даты
            (2, {"ids": "440,441"}),  # Только ids
            (
                2,
                {"startDate": "2020-10-20", "endDate": "2025-03-31", "ids": "440,441"},
            ),  # Даты и ids
        ],
    )
    async def test_statistics_districts_by_id_stat_valid(
        self, client: AsyncClient, dist_id: int, params: dict[str, str]
    ):
        """Тест эндпоинта /statistics/districts/{dist_id} с валидными параметрами"""
        response = await client.get(
            f"/api/statistics/districts/{dist_id}", params=params
        )
        # print(params, response.json())
        await assert_status_code(response, 200)
        await assert_date(response, params)

    @pytest.mark.parametrize(
        "dist_id, params, expected_status",
        [
            (-1, {}, 400),  # Неверный dist_id
            (9999, {}, 400),  # Несуществующий dist_id
            (
                1,
                {"startDate": "invalid_date", "endDate": "2025-03-31"},
                422,
            ),  # Неверный формат даты
        ],
    )
    async def test_statistics_districts_by_id_stat_invalid(
        self,
        client: AsyncClient,
        dist_id: int,
        params: dict[str, str],
        expected_status: int,
    ):
        """Тест эндпоинта /statistics/districts/{dist_id} с невалидными параметрами"""
        response = await client.get(
            f"/api/statistics/districts/{dist_id}", params=params
        )
        await assert_status_code(response, expected_status)


@pytest.mark.asyncio(loop_scope="module")
class TestDashboardEndpoints:

    @pytest.mark.parametrize(
        "params, detail",
        [
            ({}, False),  # Без параметров, без detail
            ({}, True),  # Без параметров, detail
            (
                {"startDate": "2020-10-20", "endDate": "2025-03-31"},
                False,
            ),  # Только даты
            (
                {"startDate": "2020-10-20", "endDate": "2025-03-31"},
                True,
            ),  # Только даты
        ],
    )
    async def test_dashboard_nomenclature_valid(
        self, client: AsyncClient, params: dict[str, str], detail: bool
    ):
        """Тест эндпоинта /nomenclature с валидными параметрами"""
        response = await client.get(
            "/api/dashboard/nomenclature", params={**params, "detail": detail}
        )
        await assert_status_code(response, 200)
        await assert_date(response, params)

    @pytest.mark.parametrize(
        "params, expected_status",
        [
            (
                {"startDate": "invalid_date", "endDate": "2025-03-31"},
                422,
            ),  # Неверный формат даты
            ({"detail": "invalid_detail"}, 422),  # Неверный формат ids
        ],
    )
    async def test_dashboard_nomenclature_invalid(
        self, client: AsyncClient, params: dict[str, str], expected_status: int
    ):
        """Тест эндпоинта /nomenclature с невалидными параметрами"""
        response = await client.get("/api/dashboard/nomenclature", params=params)
        await assert_status_code(response, expected_status)
        await assert_date(response, params)

    @pytest.mark.parametrize(
        "limit",
        [1, 30, 50],  # Разные значения limit
    )
    async def test_dashboard_years_valid(self, client: AsyncClient, limit: int):
        """Тест эндпоинта /years с валидными параметрами"""
        response = await client.get("/api/dashboard/years", params={"limit": limit})
        await assert_status_code(response, 200)

    @pytest.mark.parametrize(
        "limit, expected_status",
        [(-1, 422), (0, 422), (51, 422)],  # Неверные значения limit
    )
    async def test_dashboard_years_invalid(
        self, client: AsyncClient, limit: int, expected_status: int
    ):
        """Тест эндпоинта /years с невалидными параметрами"""
        response = await client.get("/api/dashboard/years", params={"limit": limit})
        await assert_status_code(response, expected_status)

    @pytest.mark.parametrize(
        "params",
        [
            {},  # Без параметров
            {"startDate": "2020-10-20", "endDate": "2025-03-31"},  # Только даты
            {"ids": "440,441"},  # Только ids
            {
                "startDate": "2020-10-20",
                "endDate": "2025-03-31",
                "ids": "440,441",
            },  # Даты и ids
        ],
    )
    async def test_dashboard_districts_valid(
        self, client: AsyncClient, params: dict[str, str]
    ):
        """Тест эндпоинта /districts с валидными параметрами"""
        response = await client.get("/api/dashboard/districts", params=params)
        await assert_status_code(response, 200)
        await assert_date(response, params)

    @pytest.mark.parametrize(
        "params, expected_status",
        [
            ({"startDate": "invalid_date"}, 422),  # Неверный формат даты
            ({"endDate": "invalid_date"}, 422),  # Неверный формат ids
        ],
    )
    async def test_dashboard_districts_invalid(
        self, client: AsyncClient, params: dict[str, str], expected_status: int
    ):
        """Тест эндпоинта /districts с невалидными параметрами"""
        response = await client.get("/api/dashboard/districts", params=params)
        await assert_status_code(response, expected_status)

    @pytest.mark.parametrize(
        "params",
        [
            {"limit": 5},  # С лимитом
            {"limit": 10, "min": 100},  # Лимит и минимальное значение
            {"limit": 10, "max": 1000},  # Лимит и максимальное значение
            {"limit": 5, "min": 50, "max": 500},  # Все параметры
        ],
    )
    async def test_dashboard_regions_valid(
        self, client: AsyncClient, params: dict[str, str]
    ):
        """Тест эндпоинта /regions с валидными параметрами"""
        response = await client.get("/api/dashboard/regions", params=params)
        await assert_status_code(response, 200)
        await assert_date(response, params)

    @pytest.mark.parametrize(
        "params, expected_status",
        [
            ({"limit": -1}, 422),  # Неверный лимит
            ({"sort": "invalid"}, 422),  # Неверный лимит
        ],
    )
    async def test_dashboard_regions_invalid(
        self, client: AsyncClient, params: dict[str, str], expected_status: int
    ):
        """Тест эндпоинта /regions с невалидными параметрами"""
        response = await client.get("/api/dashboard/regions", params=params)
        await assert_status_code(response, expected_status)

    @pytest.mark.parametrize(
        "params",
        [
            {},  # Без параметров
            {"startDate": "2020-10-20", "endDate": "2025-03-31"},  # Только даты
        ],
    )
    async def test_dashboard_types_valid(
        self, client: AsyncClient, params: dict[str, str]
    ):
        """Тест эндпоинта /types с валидными параметрами"""
        response = await client.get("/api/dashboard/types", params=params)
        await assert_status_code(response, 200)
        await assert_date(response, params)

    @pytest.mark.parametrize(
        "params, expected_status",
        [
            (
                {"startDate": "invalid_date", "endDate": "invalid_date"},
                422,
            ),  # Неверный формат даты
        ],
    )
    async def test_dashboard_types_invalid(
        self, client: AsyncClient, params: dict[str, str], expected_status: int
    ):
        """Тест эндпоинта /types с невалидными параметрами"""
        response = await client.get("/api/dashboard/types", params=params)
        await assert_status_code(response, expected_status)
