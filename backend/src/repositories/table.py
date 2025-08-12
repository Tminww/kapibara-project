from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from models import DistrictEntity, RegionEntity

from schemas import RequestTableSchema, RequestBodySchema
from database import connection
from errors import ResultIsEmptyError


class TableRepository:
    @connection
    async def get_rows_from_table_by_year(self, params:RequestTableSchema, session: AsyncSession):
        return params
    @connection
    async def get_rows_from_table_by_region(self, params:RequestTableSchema, session: AsyncSession):
        return params
        
    @connection
    async def get_rows_from_table_by_type(self, params:RequestTableSchema, session: AsyncSession):
        return params