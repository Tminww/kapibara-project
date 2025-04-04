from typing import List

from src.repositories.districts import IDistrictsRepository
from src.schemas.districts import DistrictDTO


class DistrictsService:
    def __init__(self, districts_repo: IDistrictsRepository):
        self.districts_repo: IDistrictsRepository = districts_repo()

    async def get_all_districts(self):
        districts = await self.districts_repo.get_all_districts()

        return districts

    async def get_district_by_id(self, item_id: int):
        districts = await self.districts_repo.get_district(item_id)

        return districts

    async def insert_districts(self, districts: List[DistrictDTO]) -> tuple[bool, str]:

        flag, status = await self.districts_repo.insert_or_update_districts(districts)

        return (flag, status)
