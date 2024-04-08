from abc import ABC, abstractmethod
from typing import Annotated, List

from models.districts import DistrictEntity
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from database.setup import async_session_maker


class IDistrictsRepository(ABC):
    @abstractmethod
    async def get_all_districts():
        raise NotImplementedError

    @abstractmethod
    async def insert_or_update_districts(districts: List[dict]):
        raise NotImplementedError


class DistrictsRepository(IDistrictsRepository):
    districts = DistrictEntity

    async def get_all_districts(self):

        async with async_session_maker() as session:
            stmt = select(self.districts)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            return res

    async def insert_or_update_districts(self, districts: List[dict]):
        values = [
            (district["id"], district["name"], district["short_name"])
            for district in districts
        ]
        print(districts)

        async with async_session_maker() as session:
            stmt = (
                insert(self.districts)
                .values(districts)
                .on_conflict_do_update(
                    index_elements=["id"],
                    set_=dict(
                        name=stmt.excluded.name,
                        short_name=stmt.excluded.short_name,
                    ),
                )
            )
            res = await session.execute(stmt)

            updated = res.last_updated_params
            print(updated)

            return updated
