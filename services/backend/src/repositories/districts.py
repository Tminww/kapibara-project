from abc import ABC, abstractmethod
from typing import Annotated, List

from models.districts import DistrictEntity
from schemas.districts import DistrictSchema
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from database.setup import async_session_maker


class IDistrictsRepository(ABC):
    @abstractmethod
    async def get_all_districts() -> List[DistrictSchema]:
        raise NotImplementedError

    @abstractmethod
    async def insert_or_update_districts(
        districts: List[DistrictSchema],
    ) -> tuple[bool, str]:
        raise NotImplementedError


class DistrictsRepository(IDistrictsRepository):
    districts = DistrictEntity

    async def get_all_districts(self) -> List[DistrictSchema]:

        async with async_session_maker() as session:
            stmt = select(self.districts)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            return res

    async def insert_or_update_districts(
        self, districts: List[DistrictSchema]
    ) -> tuple[bool, str]:

        values: List[dict] = []

        for district in districts:
            values.append(district.model_dump())

        async with async_session_maker() as session:
            stmt_insert = insert(self.districts).values(values)

            stmt_on_conflict = stmt_insert.on_conflict_do_update(
                index_elements=["id"],
                set_=dict(
                    name=stmt_insert.excluded.name,
                    short_name=stmt_insert.excluded.short_name,
                ),
            )

            try:
                res = await session.execute(stmt_on_conflict)
                await session.commit()
                return (True, "Success")
            except Exception as ex:
                return (False, f"Error: {ex}")
