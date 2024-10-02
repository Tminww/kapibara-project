from abc import ABC, abstractmethod
from typing import List
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert

from src.errors import ResultIsEmptyError
from src.models.types_in_block import TypesInBlockEntity
from src.schemas.types import TypesInBlockSchema
from src.database.setup import async_session_maker


class ITypesInBlockRepository(ABC):
    @abstractmethod
    async def get_all_types_in_block() -> List[TypesInBlockSchema]:
        raise NotImplementedError

    @abstractmethod
    async def get_block_by_id(id_item: int) -> List[TypesInBlockSchema]:
        raise NotImplementedError

    @abstractmethod
    async def insert_or_update_types_in_block(
        types_in_block: List[TypesInBlockSchema],
    ) -> tuple[bool, str]:
        raise NotImplementedError

    @abstractmethod
    async def delete_block(id_item: int) -> tuple[bool, str]:
        raise NotImplementedError


class TypesInBlockRepository(ITypesInBlockRepository):

    types_in_block = TypesInBlockEntity

    async def get_all_types_in_block(self) -> List[TypesInBlockSchema]:

        async with async_session_maker() as session:
            stmt = select(self.types_in_block)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                raise ResultIsEmptyError("Result is empty")

    async def get_block_by_id(self, id_item: int) -> List[TypesInBlockSchema]:

        async with async_session_maker() as session:
            stmt = select(self.types_in_block).where(self.types_in_block.id == id_item)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                raise ResultIsEmptyError("Result is empty")

    async def insert_or_update_types_in_block(
        self, types_in_block: List[TypesInBlockSchema]
    ) -> tuple[bool, str]:

        values: List[dict] = []

        for item in types_in_block:
            values.append(
                dict(id=item.id, id_block=item.block.id, id_type=item.type.id)
            )

        async with async_session_maker() as session:
            stmt_insert = insert(self.types_in_block).values(values)

            stmt_on_conflict = stmt_insert.on_conflict_do_update(
                index_elements=["id"],
                set_=dict(
                    id_block=stmt_insert.excluded.id_block,
                    id_type=stmt_insert.excluded.id_type,
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

            stmt = delete(self.types_in_block).where(self.types_in_block.id == id_item)
            try:
                res = await session.execute(stmt)
                await session.commit()
                return (True, "Success")

            except Exception as ex:
                return (False, f"Error: {ex}")
