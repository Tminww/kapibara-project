# from typing import List

# from src.repositories.regions import IRegionsRepository
# from src.schemas.regions import RegionSchema


# class RegionsService:
#     def __init__(self, regions_repo: IRegionsRepository):
#         self.regions_repo: IRegionsRepository = regions_repo()

#     async def get_all_regions(self):
#         response = []
#         regions = await self.regions_repo.get_all_regions()

#         print(response)
#         return regions

#     async def insert_blocks(self, regions: List[RegionSchema]) -> tuple[bool, str]:

#         flag, status = await self.regions_repo.insert_or_update_regions(regions)

#         return (flag, status)
