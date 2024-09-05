from typing import List

from src.repositories.types_in_block import ITypesInBlockRepository
from src.schemas.types import TypesInBlockSchema


class TypesInBlockService:
    def __init__(self, types_in_block_repo: ITypesInBlockRepository):
        self.types_in_block_repo: ITypesInBlockRepository = types_in_block_repo()

    async def get_all_types_in_block(self):
        response = []
        types_in_block = await self.types_in_block_repo.get_all_types_in_block()

        # print(response)
        return types_in_block

    async def insert_types_in_block(self, types_in_block: List[TypesInBlockSchema]) -> tuple[bool, str]:

        flag, status = await self.types_in_block_repo.insert_or_update_types_in_block(types_in_block)

        return (flag, status)
