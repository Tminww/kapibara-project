from src.schemas.subjects import SubjectsInDistrictDTO
from src.utils.repository import AbstractRepository


class SubjectsService:
    def __init__(self, subjects_repo: AbstractRepository):
        self.subjects_repo: AbstractRepository = subjects_repo()

    async def get_subjects(self):
        response = []
        districts = await self.subjects_repo.get_districts()
        for district in districts:
            regions = await self.subjects_repo.get_regions_in_district(district.id)
            response.append(
                SubjectsInDistrictDTO(
                    name=district.name, id=district.id, regions=regions
                )
            )

        print(response)
        return response
