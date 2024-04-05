from repositories.regions import IRegionsRepository


class RegionsService:
    def __init__(self, regions_repo: IRegionsRepository):
        self.regions_repo: IRegionsRepository = regions_repo()

    async def get_all_regions(self):
        response = []
        regions = await self.regions_repo.get_all_regions()

        print(response)
        return regions
