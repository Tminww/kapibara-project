from typing import List
from repositories.districts import IDistrictsRepository


class DistrictsService:
    def __init__(self, districts_repo: IDistrictsRepository):
        self.districts_repo: IDistrictsRepository = districts_repo()

    async def get_all_districts(self):
        districts = await self.districts_repo.get_all_districts()

        return districts

    async def insert_all_districts(self, districts: List[dict]):

        response = await self.districts_repo.insert_or_update_all_districts(districts)

        print(response)
        return response
