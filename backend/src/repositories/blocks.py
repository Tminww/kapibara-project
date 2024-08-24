from abc import ABC, abstractmethod
from typing import List
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert

from src.errors import ResultIsEmptyError
from src.models.blocks import BlockEntity
from src.schemas.blocks import BlockSchema
from src.database.setup import async_session_maker


class IBlocksRepository(ABC):
    @abstractmethod
    async def get_all_blocks() -> List[BlockSchema]:
        raise NotImplementedError

    @abstractmethod
    async def get_block_by_id(id_item: int) -> List[BlockSchema]:
        raise NotImplementedError

    @abstractmethod
    async def insert_or_update_blocks(
        blocks: List[BlockSchema],
    ) -> tuple[bool, str]:
        raise NotImplementedError

    @abstractmethod
    async def delete_block(id_item: int) -> tuple[bool, str]:
        raise NotImplementedError


class BlocksRepository(IBlocksRepository):

    blocks = BlockEntity

    async def get_all_blocks(self) -> List[BlockSchema]:

        async with async_session_maker() as session:
            stmt = select(self.blocks)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                raise ResultIsEmptyError("Result is empty")

    async def get_block_by_id(self, id_item: int) -> List[BlockSchema]:

        async with async_session_maker() as session:
            stmt = select(self.blocks).where(self.blocks.id == id_item)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                raise ResultIsEmptyError("Result is empty")

    async def insert_or_update_blocks(
        self, blocks: List[BlockEntity]
    ) -> tuple[bool, str]:

        values: List[dict] = []

        for block in blocks:
            print(block.model_dump())
            print(block.id, block.organ.id, block.region.id if block.region else None)
            # print(dict(id=block.id, id_organ=block.organ.id, id_reg=block.region.id))
            values.append(
                dict(
                    id=block.id,
                    id_organ=block.organ.id,
                    id_reg=block.region.id if block.region else None,
                )
            )
            print(values)

        async with async_session_maker() as session:
            stmt_insert = insert(self.blocks).values(values)

            stmt_on_conflict = stmt_insert.on_conflict_do_update(
                index_elements=["id"],
                set_=dict(
                    id_organ=stmt_insert.excluded.id_organ,
                    id_reg=stmt_insert.excluded.id_reg,
                ),
            )

            try:
                res = await session.execute(stmt_on_conflict)
                await session.commit()
                return (True, "Success")
            except Exception as ex:
                return (False, f"Error: {ex}")

    async def delete_block(self, id_item: int) -> tuple[bool, str]:

        async with async_session_maker() as session:

            stmt = delete(self.blocks).where(self.blocks.id == id_item)
            try:
                res = await session.execute(stmt)
                await session.commit()
                return (True, "Success")

            except Exception as ex:
                return (False, f"Error: {ex}")
