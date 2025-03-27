from abc import ABC, abstractmethod
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import DistrictEntity, RegionEntity

from schemas import SubjectBaseSchema, RequestBodySchema
from database.setup import connection
from errors import ResultIsEmptyError


class SubjectsRepository:
    @connection
    async def get_districts_by_regions(self, regions, session: AsyncSession):
        stmt_for_district_id = (
            select(RegionEntity.id_dist)
            .select_from(RegionEntity)
            .filter(regions is None or RegionEntity.id.in_(regions))
        )
        districts_id = await session.execute(stmt_for_district_id)
        districts_id = [row[0] for row in districts_id.all()]
        stmt = select(DistrictEntity).filter(
            regions is None or DistrictEntity.id.in_(districts_id)
        )
        res = await session.execute(stmt)
        res = [row[0] for row in res.all()]

        if res:
            return res
        else:
            raise ResultIsEmptyError("Result is empty")

    @connection
    async def get_districts(
        self,
        session: AsyncSession,
        params: RequestBodySchema = None,
    ):

        if params is None:
            stmt = select(DistrictEntity)
        else:
            stmt = select(DistrictEntity).filter(
                params.ids is None or DistrictEntity.id.in_(params.ids)
            )
        res = await session.execute(stmt)
        res = [row[0] for row in res.all()]
        if res:
            return res
        else:
            raise ResultIsEmptyError("Result is empty")

    @connection
    async def get_regions_in_district(self, id_dist, session: AsyncSession):
        stmt = select(RegionEntity).filter(RegionEntity.id_dist == id_dist)
        res = await session.execute(stmt)
        res = [SubjectBaseSchema(name=row[0].name, id=row[0].id) for row in res.all()]
        if res:
            return res
        else:
            raise ResultIsEmptyError("Result is empty")
