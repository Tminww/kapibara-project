import time

from src.schemas.statistics import (
    RequestBodySchema,
    StatAllDTO,
    StatDistrictDTO,
    StatRegionDTO,
    StatBaseDTO,
    StatRegionSchema,
    StatRegionsSchema,
)
from src.utils.repository import AbstractRepository


def get_count_from_stat(stat: list) -> int:
    count = 0
    if stat:
        for item in stat:
            count += item.count
    return count


class StatisticsService:
    def __init__(self, statistics_repo: AbstractRepository):
        self.statistics_repo: AbstractRepository = statistics_repo()

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
