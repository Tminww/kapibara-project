from sqlalchemy import Row
from typing import Sequence

from schemas import (
    RequestBodySchema,
    StatAllSchema,
    StatDistrictSchema,
    StatRegionSchema,
    StatBaseSchema,
    StatRegionSchema,
    StatPublicationSchema,
)
from repositories.statistics import StatisticsRepository
import time


def get_count_from_stat(stat: list) -> int:
    count = 0
    if stat:
        for item in stat:
            count += item.count
    return count


class StatisticsService:

    def __init__(self, repository: StatisticsRepository):
        self.repository: StatisticsRepository = repository()

    async def get_subjects(self):
        response = []
        districts = await self.repository.get_districts()
        for district in districts:
            regions = await self.repository.get_regions_in_district(district.id)
            response.append(
                StatDistrictSchema(name=district.name, id=district.id, regions=regions)
            )

        print(response)
        return response

    async def get_publication_by_types(self, params: RequestBodySchema):
        rows: Sequence[Row] = await self.repository.get_publication_by_types(params)
        stat: list[StatBaseSchema] = [
            StatBaseSchema(name=row.name, count=row.count) for row in rows
        ]

        count = get_count_from_stat(stat)
        return StatPublicationSchema(
            name="Опубликование по актам",
            stat=stat,
            count=count,
        )

    async def get_publication_by_nomenclature_detail(self, params: RequestBodySchema):
        rows: Sequence[Row] = (
            await self.repository.get_publication_by_nomenclature_detail_president_and_government(
                params
            )
        )
        stat: list[StatBaseSchema] = [
            StatBaseSchema(name=row.name, count=row.count) for row in rows
        ]

        count = get_count_from_stat(stat)
        return StatPublicationSchema(
            name="Детальное опубликование по номенклатуре",
            stat=stat,
            count=count,
        )

    async def get_publication_by_regions(self, params: RequestBodySchema):
        rows: Sequence[Row] = await self.repository.get_publication_by_regions(params)
        stat: list[StatBaseSchema] = [
            StatBaseSchema(name=row.name, count=row.count) for row in rows
        ]

        count = get_count_from_stat(stat)
        return StatPublicationSchema(
            name="Опубликование по субъектам",
            stat=stat,
            count=count,
        )

    async def get_publication_by_districts(self, params: RequestBodySchema):
        rows: Sequence[Row] = await self.repository.get_publication_by_districts(params)
        stat: list[StatBaseSchema] = [
            StatBaseSchema(name=row.name, count=row.count) for row in rows
        ]

        count = get_count_from_stat(stat)
        return StatPublicationSchema(
            name="Опубликование по федеральным округам",
            stat=stat,
            count=count,
        )

    async def get_publication_by_years(self, limit: int):
        rows: Sequence[Row] = await self.repository.get_publication_by_years(limit)
        stat: list[StatBaseSchema] = [
            StatBaseSchema(name=str(int(row.name)), count=row.count) for row in rows
        ]

        count = get_count_from_stat(stat)
        return StatPublicationSchema(
            name="Опубликование по годам", stat=stat, count=count
        )

    async def get_publication_by_nomenclature(self, params: RequestBodySchema):
        rows: Sequence[Row] = await self.repository.get_publication_by_nomenclature(
            params
        )
        stat: list[StatBaseSchema] = [
            StatBaseSchema(name=row.name, count=row.count) for row in rows
        ]

        count = get_count_from_stat(stat)
        return StatPublicationSchema(
            name="Опубликование по номенклатуре",
            stat=stat,
            count=count,
        )

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
        districts = []
        stat_all = await self.repository.get_stat_all(params)

        districts_info = await self.repository.get_districts_by_regions(params.ids)
        for district in districts_info:
            print(district)
            regions = []

            stat_in_district = await self.repository.get_stat_in_district(
                params, district.id
            )
            print(stat_in_district)
            regions_info = await self.repository.get_definite_regions_in_district(
                params, district.id
            )

            for region in regions_info:
                stat_in_region = await self.repository.get_stat_in_region(
                    params, region.id
                )

                regions.append(
                    StatRegionSchema(
                        name=region.name,
                        id=region.id,
                        count=get_count_from_stat(stat_in_region),
                        stat=stat_in_region,
                    )
                )

            districts.append(
                StatDistrictSchema(
                    name=district.name,
                    id=district.id,
                    count=get_count_from_stat(stat_in_district),
                    stat=stat_in_district,
                    regions=regions,
                )
            )

        end_time = time.time()
        print(end_time - start_time)

        return StatAllSchema(
            name="Вся статистика",
            count=get_count_from_stat(stat_all),
            stat=stat_all,
            districts=districts,
        )
