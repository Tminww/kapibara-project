from abc import ABC, abstractmethod
from typing import Annotated, List

from models.regions import RegionEntity
from schemas.regions import RegionSchema
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from database.setup import async_session_maker


class IRegionsRepository(ABC):
    @abstractmethod
    async def get_all_regions() -> List[RegionSchema]:
        raise NotImplementedError

    @abstractmethod
    async def insert_or_update_regions(regions: List[RegionSchema]) -> tuple[bool, str]:
        raise NotImplementedError


class RegionsRepository(IRegionsRepository):
    regions = RegionEntity

    async def get_all_regions(self):

        async with async_session_maker() as session:
            stmt = select(self.regions)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            return res

    async def insert_or_update_regions(
        self, regions: List[RegionSchema]
    ) -> tuple[bool, str]:

        values: List[dict] = []

        for region in regions:
            values.append(region.model_dump())

        async with async_session_maker() as session:
            stmt_insert = insert(self.regions).values(values)

            stmt_on_conflict = stmt_insert.on_conflict_do_update(
                index_elements=["external_id"],
                set_=dict(
                    name=stmt_insert.excluded.name,
                    short_name=stmt_insert.excluded.short_name,
                    code=stmt_insert.excluded.code,
                    parent_id=stmt_insert.excluded.parent_id,
                    id_dist=stmt_insert.excluded.id_dist,
                ),
            )

            try:
                res = await session.execute(stmt_on_conflict)
                await session.commit()
                return (True, "Success")
            except Exception as ex:
                return (False, f"Error: {ex}")
