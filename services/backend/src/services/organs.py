from typing import List
from repositories.organs import IOrgansRepository
from schemas.organs import OrganSchema


class OrgansService:
    def __init__(self, organs_repo: IOrgansRepository):
        self.organs_repo: IOrgansRepository = organs_repo()

    async def get_all_organs(self):
        organs = await self.organs_repo.get_all_organs()

        return organs

    async def get_organ_by_id(self, item_id: int):
        organs = await self.organs_repo.get_organ(item_id)

        return organs

    async def insert_organs(self, organs: List[OrganSchema]) -> tuple[bool, str]:

        flag, status = await self.organs_repo.insert_or_update_organs(organs)

        return (flag, status)
