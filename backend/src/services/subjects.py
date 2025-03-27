from schemas import SubjectWithRegionsSchema, RequestRegionSchema
from repositories.subjects import SubjectsRepository


class SubjectsService:

    def __init__(self, repository: SubjectsRepository):
        self.repository: SubjectsRepository = repository()

    async def get_subjects(self):
        response = []
        districts = await self.repository.get_districts()
        for district in districts:
            regions = await self.repository.get_regions_in_district(district.id)
            response.append(
                SubjectWithRegionsSchema(
                    name=district.name, id=district.id, regions=regions
                )
            )
        return response

    async def get_regions(self, params: RequestRegionSchema):
        pass

    async def get_districts(self):
        pass
