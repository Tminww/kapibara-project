from sqlalchemy import Row
from typing import Sequence

from src.schemas import (
    RequestBodySchema,
    StatAllSchema,
    StatDistrictSchema,
    StatRegionSchema,
    StatBaseSchema,
    StatRegionSchema,
    StatPublicationSchema,
)
from src.repositories.statistics import StatisticRepository
import time


def get_count_from_stat(stat: list) -> int:
    count = 0
    if stat:
        for item in stat:
            count += item.count
    return count


class StatisticService:

    def __init__(self, repository: StatisticRepository):
        self.repository: StatisticRepository = repository()

    async def get_subjects_stat(self, params: RequestBodySchema):
        stat_all = await self.repository.get_stat_all(params)

        return StatPublicationSchema(
            name="Вся статистика по субъектам",
            count=get_count_from_stat(stat_all),
            stat=stat_all,
        )

    async def get_districts_stat(self, params: RequestBodySchema):
        districts = []

        districts_info = await self.repository.get_districts(params.ids)
        for district in districts_info:
            print(district)

            stat_in_district = await self.repository.get_stat_in_district(
                params, district.id
            )
            print(stat_in_district)

            districts.append(
                StatDistrictSchema(
                    name=district.name,
                    id=district.id,
                    count=get_count_from_stat(stat_in_district),
                    stat=stat_in_district,
                )
            )

        return districts

    # async def get_stat_in_region(self, params: RequestBodySchema, id_reg):
    #     regions = []
    #     regions_info = await self.repository.get_definite_regions_in_district(
    #             params, district.id
    #     )

    #     for region in regions_info:
    #         stat_in_region = await self.repository.get_stat_in_region(
    #             params, region.id
    #         )

    #         regions.append(
    #             StatRegionSchema(
    #                 name=region.name,
    #                 id=region.id,
    #                 count=get_count_from_stat(stat_in_region),
    #                 stat=stat_in_region,
    #             )
    #         )

    async def get_stat_in_districts(self, params: RequestBodySchema):
        start_time = time.time()

        # Получаем все данные одним запросом
        stat_data = await self.repository.get_stat_in_districts(params)

        districts = []

        # Получаем информацию об округах
        districts_info = await self.repository.get_districts_by_regions(params.ids)

        # Формируем ответ
        for district in districts_info:
            district_id = district.id
            district_stats = stat_data["districts"].get(district_id, {})

            regions = []
            for region_id, region_data in district_stats.get("regions", {}).items():
                regions.append(
                    StatRegionSchema(
                        id=region_id,
                        name=region_data["name"],  # Используем сохраненное имя
                        count=sum(region_data["stats"].values()),
                        stat=[
                            StatBaseSchema(name=k, count=v)
                            for k, v in region_data["stats"].items()
                        ],
                    )
                )

            districts.append(
                StatDistrictSchema(
                    id=district_id,
                    name=district.name,
                    count=sum(district_stats.get("total", {}).values()),
                    stat=[
                        StatBaseSchema(name=k, count=v)
                        for k, v in district_stats.get("total", {}).items()
                    ],
                    regions=regions,
                )
            )

        return StatAllSchema(
            name="Вся статистика",
            count=sum(stat_data["total"].values()),
            stat=[
                StatBaseSchema(name=k, count=v) for k, v in stat_data["total"].items()
            ],
            districts=districts,
        )

    ## USE
    async def get_regions_in_district(self, dist_id: int, params: RequestBodySchema):
        districts = []

        districts_info = await self.repository.get_districts(dist_id)
        for district in districts_info:
            print(district)

            stat_in_district = await self.repository.get_stat_in_district(
                params, district.id
            )
            print(stat_in_district)

            districts.append(
                StatDistrictSchema(
                    name=district.name,
                    id=district.id,
                    count=get_count_from_stat(stat_in_district),
                    stat=stat_in_district,
                )
            )

        return districts
