from typing import List

from src.repositories.blocks import IBlocksRepository
from src.schemas.blocks import BlockSchema


class BlocksService:
    def __init__(self, blocks_repo: IBlocksRepository):
        self.blocks_repo: IBlocksRepository = blocks_repo()

    async def get_all_blocks(self):
        response = []
        blocks = await self.blocks_repo.get_all_blocks()

        print(response)
        return blocks

    async def insert_blocks(self, blocks: List[BlockSchema]) -> tuple[bool, str]:

        flag, status = await self.blocks_repo.insert_or_update_blocks(blocks)

        return (flag, status)
