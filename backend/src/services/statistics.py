from sqlalchemy import Row
from typing import Sequence

from schemas.subjects import RegionsInDistrictDTO
from schemas.statistics import (
    RequestBodySchema,
    StatAllDTO,
    StatDistrictDTO,
    StatRegionDTO,
    SubjectsStatDTO,
    DistrictsStatDTO,
    DistrictStatDTO,
    StatBaseDTO,
    StatRegionSchema,
    StatRegionsSchema,
    ResponseStatDTO,
)
from repositories.statistics import SQLAlchemyRepository
import time


def get_count_from_stat(stat: list) -> int:
    count = 0
    if stat:
        for item in stat:
            count += item.count
    return count


class StatisticsService:
    def __init__(self, statistics_repo: SQLAlchemyRepository):
        self.statistics_repo: SQLAlchemyRepository = statistics_repo()

    async def get_subjects(self):
        response = []
        districts = await self.statistics_repo.get_districts()
        for district in districts:
            regions = await self.statistics_repo.get_regions_in_district(district.id)
            response.append(
                RegionsInDistrictDTO(
                    name=district.name, id=district.id, regions=regions
                )
            )

        print(response)
        return response

    
    async def get_publication_by_acts(self, parameters: RequestBodySchema):
        rows: Sequence[Row] = (
            await self.statistics_repo.get_publication_by_acts(
                parameters
            )
        )
        stat: list[StatBaseDTO] = [
            StatBaseDTO(name=row.name, count=row.count) for row in rows
        ]

        start_date: str | None = (
            parameters.start_date if parameters.start_date is not None else None
        )
        end_date: str | None = (
            parameters.end_date if parameters.end_date is not None else None
        )
        count = get_count_from_stat(stat)
        return ResponseStatDTO(
            name="Опубликование по актам",
            startDate=start_date,
            endDate=end_date,
            stat=stat,
            count=count,
        )
    
    async def get_publication_by_nomenclature_detail(
        self, parameters: RequestBodySchema
    ):
        rows: Sequence[Row] = (
            await self.statistics_repo.get_publication_by_nomenclature_detail_president_and_government(
                parameters
            )
        )
        stat: list[StatBaseDTO] = [
            StatBaseDTO(name=row.name, count=row.count) for row in rows
        ]

        start_date: str | None = (
            parameters.start_date if parameters.start_date is not None else None
        )
        end_date: str | None = (
            parameters.end_date if parameters.end_date is not None else None
        )
        count = get_count_from_stat(stat)
        return ResponseStatDTO(
            name="Детальное опубликование по номенклатуре",
            startDate=start_date,
            endDate=end_date,
            stat=stat,
            count=count,
        )

    async def get_publication_by_regions(self, parameters: RequestBodySchema):
        rows: Sequence[Row] = await self.statistics_repo.get_publication_by_regions(
            parameters
        )
        stat: list[StatBaseDTO] = [
            StatBaseDTO(name=row.name, count=row.count) for row in rows
        ]

        start_date: str | None = (
            parameters.start_date if parameters.start_date is not None else None
        )
        end_date: str | None = (
            parameters.end_date if parameters.end_date is not None else None
        )
        count = get_count_from_stat(stat)
        return ResponseStatDTO(
            name="Опубликование по субъектам",
            startDate=start_date,
            endDate=end_date,
            stat=stat,
            count=count,
        )

    async def get_publication_by_districts(self, parameters: RequestBodySchema):
        rows: Sequence[Row] = await self.statistics_repo.get_publication_by_districts(
            parameters
        )
        stat: list[StatBaseDTO] = [
            StatBaseDTO(name=row.name, count=row.count) for row in rows
        ]

        start_date: str | None = (
            parameters.start_date if parameters.start_date is not None else None
        )
        end_date: str | None = (
            parameters.end_date if parameters.end_date is not None else None
        )
        count = get_count_from_stat(stat)
        return ResponseStatDTO(
            name="Опубликование по федеральным округам",
            startDate=start_date,
            endDate=end_date,
            stat=stat,
            count=count,
        )

    async def get_publication_by_years(self, limit: int):
        rows: Sequence[Row] = await self.statistics_repo.get_publication_by_years(limit)
        stat: list[StatBaseDTO] = [
            StatBaseDTO(name=str(int(row.name)), count=row.count) for row in rows
        ]

        count = get_count_from_stat(stat)
        return ResponseStatDTO(name="Опубликование по годам", stat=stat, count=count)

    async def get_publication_by_nomenclature(self, parameters: RequestBodySchema):
        rows: Sequence[Row] = (
            await self.statistics_repo.get_publication_by_nomenclature(parameters)
        )
        stat: list[StatBaseDTO] = [
            StatBaseDTO(name=row.name, count=row.count) for row in rows
        ]

        start_date: str | None = (
            parameters.start_date if parameters.start_date is not None else None
        )
        end_date: str | None = (
            parameters.end_date if parameters.end_date is not None else None
        )
        count = get_count_from_stat(stat)
        return ResponseStatDTO(
            name="Опубликование по номенклатуре",
            startDate=start_date,
            endDate=end_date,
            stat=stat,
            count=count,
        )

    async def get_subjects_stat(self, parameters: RequestBodySchema):
        stat_all = await self.statistics_repo.get_stat_all(parameters)

        return SubjectsStatDTO(
            name="Вся статистика по субъектам",
            count=get_count_from_stat(stat_all),
            stat=stat_all,
        )

    async def get_districts_stat(self, parameters: RequestBodySchema):
        districts = []

        districts_info = await self.statistics_repo.get_districts(
            parameters.regions
        )
        for district in districts_info:
            print(district)

            stat_in_district = await self.statistics_repo.get_stat_in_district(
                parameters, district.id
            )
            print(stat_in_district)

            districts.append(
                DistrictStatDTO(
                    name=district.name,
                    id=district.id,
                    count=get_count_from_stat(stat_in_district),
                    stat=stat_in_district,
                )
            )

        return districts

    # async def get_stat_in_region(self, parameters: RequestBodySchema, id_reg):
    #     regions = []
    #     regions_info = await self.statistics_repo.get_definite_regions_in_district(
    #             parameters, district.id
    #     )

    #     for region in regions_info:
    #         stat_in_region = await self.statistics_repo.get_stat_in_region(
    #             parameters, region.id
    #         )

    #         regions.append(
    #             StatRegionDTO(
    #                 name=region.name,
    #                 id=region.id,
    #                 count=get_count_from_stat(stat_in_region),
    #                 stat=stat_in_region,
    #             )
    #         )

    async def get_stat_in_districts(self, parameters: RequestBodySchema):
        start_time = time.time()
        districts = []
        stat_all = await self.statistics_repo.get_stat_all(parameters)

        districts_info = await self.statistics_repo.get_districts_by_regions(
            parameters.regions
        )
        for district in districts_info:
            print(district)
            regions = []

            stat_in_district = await self.statistics_repo.get_stat_in_district(
                parameters, district.id
            )
            print(stat_in_district)
            regions_info = await self.statistics_repo.get_definite_regions_in_district(
                parameters, district.id
            )

            for region in regions_info:
                stat_in_region = await self.statistics_repo.get_stat_in_region(
                    parameters, region.id
                )

                regions.append(
                    StatRegionDTO(
                        name=region.name,
                        id=region.id,
                        count=get_count_from_stat(stat_in_region),
                        stat=stat_in_region,
                    )
                )

            districts.append(
                StatDistrictDTO(
                    name=district.name,
                    id=district.id,
                    count=get_count_from_stat(stat_in_district),
                    stat=stat_in_district,
                    regions=regions,
                )
            )

        end_time = time.time()
        print(end_time - start_time)

        return StatAllDTO(
            name="Вся статистика",
            count=get_count_from_stat(stat_all),
            stat=stat_all,
            districts=districts,
        )
