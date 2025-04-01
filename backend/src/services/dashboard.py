from sqlalchemy import Row
from typing import Sequence

from schemas import (
    RequestBodySchema,
    StatBaseSchema,
    StatPublicationSchema,
)
from repositories import DashboardRepository


def get_count_from_stat(stat: list) -> int:
    count = 0
    if stat:
        for item in stat:
            count += item.count
    return count


class DashboardService:

    def __init__(self, repository: DashboardRepository):
        self.repository: DashboardRepository = repository()

    async def get_publication_by_types(self, params: RequestBodySchema):
        rows: Sequence[Row] = await self.repository.get_publication_by_types(params)
        stat: list[StatBaseSchema] = [
            StatBaseSchema(name=row.name, count=row.count) for row in rows
        ]

        count = get_count_from_stat(stat)
        return StatPublicationSchema(
            name="Опубликование по актам",
            stat=stat,
            count=count,
        )

    async def get_publication_by_nomenclature_detail(self, params: RequestBodySchema):
        rows: Sequence[Row] = (
            await self.repository.get_publication_by_nomenclature_detail_president_and_government(
                params
            )
        )
        stat: list[StatBaseSchema] = [
            StatBaseSchema(name=row.name, count=row.count) for row in rows
        ]

        count = get_count_from_stat(stat)
        return StatPublicationSchema(
            name="Детальное опубликование по номенклатуре",
            stat=stat,
            count=count,
        )

    async def get_publication_by_regions(self, params: RequestBodySchema):
        rows: Sequence[Row] = await self.repository.get_publication_by_regions(params)
        stat: list[StatBaseSchema] = [
            StatBaseSchema(name=row.name, count=row.count) for row in rows
        ]

        count = get_count_from_stat(stat)
        return StatPublicationSchema(
            name="Опубликование по субъектам",
            stat=stat,
            count=count,
        )

    async def get_publication_by_districts(self, params: RequestBodySchema):
        rows: Sequence[Row] = await self.repository.get_publication_by_districts(params)
        stat: list[StatBaseSchema] = [
            StatBaseSchema(name=row.name, count=row.count) for row in rows
        ]

        count = get_count_from_stat(stat)
        return StatPublicationSchema(
            name="Опубликование по федеральным округам",
            stat=stat,
            count=count,
        )

    async def get_publication_by_years(self, limit: int):
        rows: Sequence[Row] = await self.repository.get_publication_by_years(limit)
        stat: list[StatBaseSchema] = [
            StatBaseSchema(name=str(int(row.name)), count=row.count) for row in rows
        ]

        count = get_count_from_stat(stat)
        return StatPublicationSchema(
            name="Опубликование по годам", stat=stat, count=count
        )

    async def get_publication_by_nomenclature(self, params: RequestBodySchema):
        rows: Sequence[Row] = await self.repository.get_publication_by_nomenclature(
            params
        )
        stat: list[StatBaseSchema] = [
            StatBaseSchema(name=row.name, count=row.count) for row in rows
        ]

        count = get_count_from_stat(stat)
        return StatPublicationSchema(
            name="Опубликование по номенклатуре",
            stat=stat,
            count=count,
        )
