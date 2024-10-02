from abc import ABC, abstractmethod
from typing import List
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert

from src.errors import ResultIsEmptyError
from src.models.deadlines import DeadlineEntity
from src.schemas.deadlines import DeadlinesSchema
from src.database.setup import async_session_maker


class IDeadlinesRepository(ABC):
    @abstractmethod
    async def get_all_deadlines() -> List[DeadlinesSchema]:
        raise NotImplementedError

    @abstractmethod
    async def get_deadline(id_item: int) -> List[DeadlinesSchema]:
        raise NotImplementedError

    @abstractmethod
    async def insert_or_update_deadlines(
        deadlines: List[DeadlinesSchema],
    ) -> tuple[bool, str]:
        raise NotImplementedError

    @abstractmethod
    async def delete_deadline(id_item: int) -> tuple[bool, str]:
        raise NotImplementedError


class DeadlinesRepository(IDeadlinesRepository):

    deadlines = DeadlineEntity

    async def get_all_deadlines(self) -> List[DeadlinesSchema]:

        async with async_session_maker() as session:
            stmt = select(self.deadlines)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                raise ResultIsEmptyError("Result is empty")

    async def get_deadline(self, id_item: int) -> List[DeadlinesSchema]:

        async with async_session_maker() as session:
            stmt = select(self.deadlines).where(self.deadlines.id == id_item)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                raise ResultIsEmptyError("Result is empty")

    async def insert_or_update_deadlines(
        self, deadlines: List[DeadlineEntity]
    ) -> tuple[bool, str]:

        values: List[dict] = []

        for deadline in deadlines:
            values.append(deadline.model_dump())

        async with async_session_maker() as session:
            stmt_insert = insert(self.deadlines).values(values)

            stmt_on_conflict = stmt_insert.on_conflict_do_update(
                index_elements=["id"],
                set_=dict(
                    day=stmt_insert.excluded.day,
                ),
            )

            try:
                res = await session.execute(stmt_on_conflict)
                await session.commit()
                return (True, "Success")
            except Exception as ex:
                return (False, f"Error: {ex}")

    async def delete_deadline(self, id_item: int) -> tuple[bool, str]:

        async with async_session_maker() as session:

            stmt = delete(self.deadlines).where(self.deadlines.id == id_item)
            try:
                res = await session.execute(stmt)
                await session.commit()
                return (True, "Success")

            except Exception as ex:
                return (False, f"Error: {ex}")
