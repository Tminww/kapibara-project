from abc import ABC, abstractmethod
from typing import Annotated, List

from models.regions import RegionEntity
from schemas.regions import RegionSchema
from sqlalchemy import select

from database.setup import async_session_maker


class IRegionsRepository(ABC):
    @abstractmethod
    async def get_all_regions() -> List[RegionSchema]:
        raise NotImplementedError
    async def insert_or_update_regions():



class RegionsRepository(IRegionsRepository):
    regions = RegionEntity

    async def get_all_regions(self):

        async with async_session_maker() as session:
            stmt = select(self.regions)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            return res
