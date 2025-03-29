from collections import defaultdict

from sqlalchemy import (
    Date,
    and_,
    cast,
    select,
    func,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import (
    TypeEntity,
    DistrictEntity,
    DocumentEntity,
    RegionEntity,
)

from src.schemas import (
    RegionSchema,
    RegionInfoSchema,
    RequestMaxMinBodySchema,
    StatBaseSchema,
    RequestBodySchema,
)
from src.database.setup import connection
from src.errors import ResultIsEmptyError


class StatisticRepository:
    @connection
    async def get_definite_regions_in_district(
        self, params: RequestBodySchema, id_dist, session: AsyncSession
    ):

        print(params.ids)

        stmt = select(RegionEntity).filter(
            (params.ids is None or RegionEntity.id.in_(params.ids)),
            (RegionEntity.id_dist == id_dist),
        )
        res = await session.execute(stmt)

        res = [row[0] for row in res.all()]

        if res:
            return res
        else:
            raise ResultIsEmptyError("Result is empty")

    @connection
    async def get_stat_all(self, params: RequestBodySchema, session: AsyncSession):

        print(params.ids)

        stmt = (
            select(
                TypeEntity.name.label("name"),
                func.count().label("count"),
            )
            .select_from(DocumentEntity)
            .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
            .join(TypeEntity, DocumentEntity.id_type == TypeEntity.id)
            .filter(
                (params.ids is None or RegionEntity.id.in_(params.ids)),
                (
                    params.start_date is None
                    and params.end_date is None
                    or DocumentEntity.view_date.between(
                        params.start_date, params.end_date
                    )
                ),
            )
            .group_by(TypeEntity.name)
            .order_by(TypeEntity.name)
        )
        res = await session.execute(stmt)
        print(res)
        res = [StatBaseSchema(name=row.name, count=row.count) for row in res.all()]
        print(res)
        if res:
            return res
        else:
            print("get_stat_all")
            raise ResultIsEmptyError("Result is empty")

    @connection
    async def get_stat_in_district(
        self, params: RequestBodySchema, id_dist, session: AsyncSession
    ):

        stmt = (
            select(
                TypeEntity.name.label("name"),
                func.count().label("count"),
            )
            .select_from(DocumentEntity)
            .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
            .join(TypeEntity, DocumentEntity.id_type == TypeEntity.id)
            .filter(
                (RegionEntity.id_dist == id_dist),
                (params.ids is None or RegionEntity.id.in_(params.ids)),
                (
                    params.start_date is None
                    and params.end_date is None
                    or DocumentEntity.view_date.between(
                        params.start_date, params.end_date
                    )
                ),
            )
            .group_by(TypeEntity.name)
            .order_by(TypeEntity.name)
        )
        res = await session.execute(stmt)
        res = [StatBaseSchema(name=row.name, count=row.count) for row in res.all()]

        return res
        # if res:
        #     return res
        # else:
        #     raise ResultIsEmptyError("Result is empty")

    # @connection
    # async def get_stat_in_districts(
    #     self, params: RequestBodySchema, session: AsyncSession
    # ):

    #     stmt = (
    #         select(
    #             TypeEntity.name.label("name"),
    #             func.count().label("count"),
    #         )
    #         .select_from(DocumentEntity)
    #         .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
    #         .join(TypeEntity, DocumentEntity.id_type == TypeEntity.id)
    #         .filter(
    #             (params.ids is None or RegionEntity.id_dist.in_(params.ids)),
    #             (
    #                 params.start_date is None
    #                 and params.end_date is None
    #                 or DocumentEntity.view_date.between(
    #                     params.start_date, params.end_date
    #                 )
    #             ),
    #         )
    #         .group_by(TypeEntity.name)
    #         .order_by(TypeEntity.name)
    #     )
    #     res = await session.execute(stmt)
    #     res = [StatBaseSchema(name=row.name, count=row.count) for row in res.all()]

    #     return res
    #     # if res:
    #     #     return res
    #     # else:
    #     #     raise ResultIsEmptyError("Result is empty")

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
            print("get_stat_in_district")
            raise ResultIsEmptyError("Result is empty")

    @connection
    async def get_districts(
        self, session: AsyncSession, params: RequestBodySchema = None
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
            print("get_districts")
            raise ResultIsEmptyError("Result is empty")

    @connection
    async def get_regions_in_district(self, id_dist, session: AsyncSession):
        stmt = select(RegionEntity).filter(RegionEntity.id_dist == id_dist)
        res = await session.execute(stmt)

        res = [RegionInfoSchema(name=row[0].name, id=row[0].id) for row in res.all()]

        if res:
            return res
        else:
            print("get_regions_in_district")
            raise ResultIsEmptyError("Result is empty")

    @connection
    async def get_stat_in_region(
        self, params: RequestBodySchema, id_reg, session: AsyncSession
    ):

        stmt = (
            select(
                TypeEntity.name.label("name"),
                func.count().label("count"),
            )
            .select_from(DocumentEntity)
            .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
            .join(TypeEntity, DocumentEntity.id_type == TypeEntity.id)
            .filter(
                (RegionEntity.id == id_reg),
                (
                    params.start_date is None
                    and params.end_date is None
                    or DocumentEntity.view_date.between(
                        params.start_date, params.end_date
                    )
                ),
            )
            .group_by(TypeEntity.name)
            .order_by(TypeEntity.name)
        )
        res = await session.execute(stmt)
        res = [StatBaseSchema(name=row.name, count=row.count) for row in res.all()]

        # if res:
        #     return res
        # else:
        #     raise ResultIsEmptyError("Result is empty")
        return res

    async def _base_stat_query(self, params: RequestBodySchema):
        """Базовый запрос для статистики с фильтрами"""
        query = (
            select(
                RegionEntity.id_dist,
                RegionEntity.id.label("region_id"),
                RegionEntity.name.label("region_name"),  # Добавляем имя региона
                TypeEntity.name.label("type_name"),
                func.count().label("count"),
            )
            .select_from(DocumentEntity)
            .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
            .join(TypeEntity, DocumentEntity.id_type == TypeEntity.id)
            .group_by(
                RegionEntity.id_dist,
                RegionEntity.id,
                TypeEntity.name,
                RegionEntity.name,
            )
        )

        # Фильтры по датам
        date_filters = []
        if params.start_date:
            date_filters.append(
                DocumentEntity.view_date >= cast(params.start_date, Date)
            )
        if params.end_date:
            date_filters.append(DocumentEntity.view_date <= cast(params.end_date, Date))

        if date_filters:
            query = query.filter(and_(*date_filters))

        # Фильтр по регионам
        if params.ids:
            query = query.filter(RegionEntity.id.in_(params.ids))

        return query

    @connection
    async def get_stat_data(self, params: RequestBodySchema, session: AsyncSession):
        """Основной запрос для получения всей статистики"""
        query = await self._base_stat_query(params)
        result = await session.execute(query)
        return result.all()

    @connection
    async def get_stat_in_districts(
        self, params: RequestBodySchema, session: AsyncSession
    ):
        """Получение агрегированных данных для всех уровней"""
        all_data = await self.get_stat_data(params)

        result = {
            "total": defaultdict(int),
            "districts": defaultdict(
                lambda: {
                    "total": defaultdict(int),
                    "regions": defaultdict(
                        lambda: {
                            "name": "",  # Добавляем поле для имени
                            "stats": defaultdict(int),
                        }
                    ),
                }
            ),
        }

        for row in all_data:
            district_id = row.id_dist
            region_id = row.region_id
            region_name = row.region_name  # Получаем имя из результата запроса
            type_name = row.type_name
            count = row.count

            # Сохраняем имя региона
            result["districts"][district_id]["regions"][region_id]["name"] = region_name

            # Обновляем статистику
            result["total"][type_name] += count
            result["districts"][district_id]["total"][type_name] += count
            result["districts"][district_id]["regions"][region_id]["stats"][
                type_name
            ] += count

        return result

    # Остальные методы адаптируются под новую структуру
