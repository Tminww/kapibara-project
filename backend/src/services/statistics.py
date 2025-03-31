from src.schemas import (
    StatAllSchema,
    RequestBodySchema,
    ResponseStatSchema,
)
from src.errors import ResultIsEmptyError
from src.repositories import StatisticRepository


class StatisticService:
    def __init__(self, repository: StatisticRepository):
        self.repository: StatisticRepository = repository()

    async def get_stat_in_districts(self, params: RequestBodySchema) -> StatAllSchema:
        """
        Получение полной статистики с детализацией по округам и регионам
        """

        try:
            result = await self.repository.get_stat_in_districts(params)
            return result
        except Exception as e:
            # Логирование ошибки
            print(f"Error in get_stat_in_districts: {e}")
            raise ResultIsEmptyError("Не удалось получить статистику")

    async def get_stat_districts(self, params: RequestBodySchema) -> StatAllSchema:
        """
        Получение статистики только по округам без детализации по регионам
        """
        try:
            result = await self.repository.get_statistics_districts(params)
            return result
        except Exception as e:
            # Логирование ошибки
            print(f"Error in get_districts_stat: {e}")
            raise ResultIsEmptyError("Не удалось получить статистику по округам")

    async def get_stat_districts_by_id(
        self, district_id: int, params: RequestBodySchema
    ) -> StatAllSchema:
        """
        Получение статистики по регионам конкретного округа
        """
        try:
            result = await self.repository.get_statistics_district_by_id(
                district_id, params
            )
            return result
        except Exception as e:
            # Логирование ошибки
            print(f"Error in get_regions_in_district: {e}")
            raise ResultIsEmptyError(
                f"Не удалось получить статистику для округа {district_id}"
            )
