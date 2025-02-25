from sqlalchemy import Row
from typing import Sequence

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
    ResponseStatDTO
)
from utils.repository import AbstractRepository
import time


def get_count_from_stat(stat: list) -> int:
    count = 0
    if stat:
        for item in stat:
            count += item.count
    return count


class StatisticsService:
    def __init__(self, statistics_repo: AbstractRepository):
        self.statistics_repo: AbstractRepository = statistics_repo()

    async def get_publication_by_nomenclature(self, parameters: RequestBodySchema):
        rows: Sequence[Row]  = await self.statistics_repo.get_publication_by_nomenclature(parameters)
        stat: list[StatBaseDTO] = [StatBaseDTO(name= row.name, count= row.count) for row in rows]
        
        start_date: str | None = parameters.start_date if parameters.start_date is not None else None 
        end_date: str | None = parameters.end_date if parameters.end_date is not None else None
        count = get_count_from_stat(stat)
        return ResponseStatDTO(name="Опубликование по номенклатуре", startDate=start_date, endDate=end_date, stat=stat, count = count)
    
    async def get_subjects_stat(self, parameters: RequestBodySchema):
        stat_all = await self.statistics_repo.get_stat_all(parameters)
        
        return SubjectsStatDTO(
            name="Вся статистика по субъектам",
            count=get_count_from_stat(stat_all),
            stat=stat_all,
            
        )
    
    async def get_districts_stat(self, parameters: RequestBodySchema):
        districts = []

        districts_info = await self.statistics_repo.get_districts_by_regions(
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
