from abc import ABC, abstractmethod
from typing import Annotated, List

from errors import ResultIsEmptyError
from models.organs import OrganEntity
from schemas.organs import OrganSchema
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from database.setup import async_session_maker


class IOrgansRepository(ABC):
    @abstractmethod
    async def get_all_organs() -> List[OrganSchema]:
        raise NotImplementedError

    async def get_organ(id_item: int) -> List[OrganSchema]:
        raise NotImplementedError

    @abstractmethod
    async def insert_or_update_organs(
        organs: List[OrganSchema],
    ) -> tuple[bool, str]:
        raise NotImplementedError


class OrgansRepository(IOrgansRepository):
    organs = OrganEntity

    async def get_all_organs(self) -> List[OrganSchema]:

        async with async_session_maker() as session:
            stmt = select(self.organs)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                raise ResultIsEmptyError("Result is empty")

    async def get_organ(self, item_id: int) -> List[OrganSchema]:

        async with async_session_maker() as session:
            stmt = select(self.organs).where(self.organs.id == item_id)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                raise ResultIsEmptyError("Result is empty")

    async def insert_or_update_organs(
        self, organs: List[OrganSchema]
    ) -> tuple[bool, str]:

        values: List[dict] = []

        for organ in organs:
            values.append(organ.model_dump())

        async with async_session_maker() as session:
            stmt_insert = insert(self.organs).values(values)

            stmt_on_conflict = stmt_insert.on_conflict_do_update(
                index_elements=["id"],
                set_=dict(
                    name=stmt_insert.excluded.name,
                    short_name=stmt_insert.excluded.short_name,
                    external_id=stmt_insert.excluded.external_id,
                    code=stmt_insert.excluded.code,
                    parent_id=stmt_insert.excluded.parent_id,
                ),
            )

            try:
                res = await session.execute(stmt_on_conflict)
                await session.commit()
                return (True, "Success")
            except Exception as ex:
                return (False, f"Error: {ex}")
