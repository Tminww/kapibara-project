from schemas import SubjectWithRegionsSchema, RequestRegionSchema, SubjectBaseSchema
from repositories.subjects import SubjectRepository


class SubjectService:

    def __init__(self, repository: SubjectRepository):
        self.repository: SubjectRepository = repository()

    async def get_subjects(self):
        response = []
        districts = await self.repository.get_districts()
        for district in districts:
            regions = await self.repository.get_regions_in_district_by_id(district.id)
            response.append(
                SubjectWithRegionsSchema(
                    name=district.name, id=district.id, regions=regions
                )
            )
        return response

    async def get_regions(self, params: RequestRegionSchema):
        if params.districtName is None and params.districtId is None:
            regions = await self.repository.get_regions()
        elif params.districtId is not None:
            regions = await self.repository.get_regions_in_district_by_id(
                params.districtId
            )
        elif params.districtName is not None:
            regions = await self.repository.get_regions_in_district_by_name(
                params.districtName
            )

        return regions

    async def get_districts(self):
        districts = await self.repository.get_districts()

        return [SubjectBaseSchema(id=d.id, name=d.name) for d in districts]
