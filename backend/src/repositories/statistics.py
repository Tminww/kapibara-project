from datetime import datetime

from sqlalchemy import (
    Date,
    and_,
    cast,
    select,
    func,
    text,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import (
    TypeEntity,
    DistrictEntity,
    DocumentEntity,
    RegionEntity,
)

from schemas import (
    RegionSchema,
    RegionInfoSchema,
    RequestMaxMinBodySchema,
    StatBaseSchema,
    RequestBodySchema,
    StatAllSchema,
    StatDistrictSchema,
    StatRegionSchema,
)
from database.setup import connection
from errors import ResultIsEmptyError


class StatisticRepository:

    async def _base_stat_query(self, params: RequestBodySchema):
        """Оптимизированный базовый запрос для статистики с фильтрами"""
        # Преобразуем даты заранее, если они есть
        start_date = None
        end_date = None
        if params.start_date and params.end_date:
            try:
                # Преобразование строк в объекты даты один раз вместо использования func.to_date в SQL
                start_date = datetime.strptime(params.start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(params.end_date, "%Y-%m-%d").date()
            except ValueError:
                # Обработка случая неверного формата даты
                pass

        # Основной запрос остается тем же, но с улучшенной оптимизацией
        query = (
            select(
                RegionEntity.id_dist,
                RegionEntity.id.label("region_id"),
                RegionEntity.name.label("region_name"),
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

        if start_date and end_date:
            # Использование объектов даты напрямую вместо функции to_date
            query = query.filter(DocumentEntity.view_date.between(start_date, end_date))

        # Фильтр по регионам
        if params.ids:
            query = query.filter(RegionEntity.id.in_(params.ids))

        return query

    @connection
    async def get_combined_stat_data(
        self, params: RequestBodySchema, session: AsyncSession
    ):
        """Получение статистики и информации об округах одним запросом"""
        # Получаем статистику
        query = await self._base_stat_query(params)

        # Для улучшения производительности, добавим подсказку для планировщика запросов
        # Это может помочь БД выбрать более эффективный план выполнения
        # query = query.with_hint(DocumentEntity, "USE INDEX (idx_documents_view_date, idx_documents_id_reg)")

        result = await session.execute(query)
        stat_data = result.all()

        # Получаем информацию об округах в одном запросе вместо отдельного
        districts_query = select(DistrictEntity).join(
            RegionEntity, RegionEntity.id_dist == DistrictEntity.id
        )

        if params.ids:
            districts_query = districts_query.filter(RegionEntity.id.in_(params.ids))

        districts_result = await session.execute(districts_query)
        districts_data = districts_result.scalars().all()

        return stat_data, {d.id: d for d in districts_data}

    @connection
    async def get_districts_stat_data(
        self, params: RequestBodySchema, session: AsyncSession
    ):
        """Оптимизированное получение статистики только по округам"""
        # Преобразуем даты заранее
        start_date = None
        end_date = None
        if params.start_date and params.end_date:
            try:
                start_date = datetime.strptime(params.start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(params.end_date, "%Y-%m-%d").date()
            except ValueError:
                pass

        # Эффективный запрос статистики по округам без детализации по регионам
        query = (
            select(
                RegionEntity.id_dist,
                TypeEntity.name.label("type_name"),
                func.count().label("count"),
            )
            .select_from(DocumentEntity)
            .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
            .join(TypeEntity, DocumentEntity.id_type == TypeEntity.id)
            .group_by(
                RegionEntity.id_dist,
                TypeEntity.name,
            )
        )

        if start_date and end_date:
            query = query.filter(DocumentEntity.view_date.between(start_date, end_date))

        # Фильтр по округам через регионы
        if params.ids:
            query = query.filter(RegionEntity.id.in_(params.ids))

        result = await session.execute(query)

        stat_data = result.all()

        # Получаем информацию об округах
        districts_query = select(DistrictEntity)

        districts_result = await session.execute(districts_query)
        districts_data = {d.id: d for d in districts_result.scalars().all()}

        return stat_data, districts_data

    @connection
    async def get_regions_in_district_data(
        self, district_id: int, params: RequestBodySchema, session: AsyncSession
    ):
        """Получение данных для статистики по регионам конкретного округа"""
        # Преобразуем даты заранее
        start_date = None
        end_date = None
        if params.start_date and params.end_date:
            try:
                start_date = datetime.strptime(params.start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(params.end_date, "%Y-%m-%d").date()
            except ValueError:
                pass

        # Запрос статистики только для регионов указанного округа
        query = (
            select(
                RegionEntity.id.label("region_id"),
                RegionEntity.name.label("region_name"),
                TypeEntity.name.label("type_name"),
                func.count().label("count"),
            )
            .select_from(DocumentEntity)
            .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
            .join(TypeEntity, DocumentEntity.id_type == TypeEntity.id)
            .filter(RegionEntity.id_dist == district_id)
            .group_by(
                RegionEntity.id,
                TypeEntity.name,
                RegionEntity.name,
            )
        )

        if start_date and end_date:
            query = query.filter(DocumentEntity.view_date.between(start_date, end_date))

        # Фильтр по регионам
        if params.ids:
            query = query.filter(RegionEntity.id.in_(params.ids))

        result = await session.execute(query)
        stat_data = result.all()

        # Получаем информацию об округе
        district_query = select(DistrictEntity).filter(DistrictEntity.id == district_id)
        district_result = await session.execute(district_query)
        district_data = district_result.scalar_one_or_none()

        return stat_data, district_data

    async def get_stat_in_districts(self, params: RequestBodySchema):
        """Оптимизированная функция для получения статистики по округам с регионами"""
        # Получаем все данные одним запросом
        all_data, districts_info = await self.get_combined_stat_data(params)

        # Используем словарь для быстрого доступа вместо defaultdict для лучшей производительности
        result = {"total": {}, "districts": {}}

        # Предварительно инициализируем структуру для предотвращения многократного создания словарей
        for row in all_data:
            district_id = row.id_dist
            region_id = row.region_id
            type_name = row.type_name
            count = row.count

            # Инициализируем структуру, если еще не создана
            if district_id not in result["districts"]:
                result["districts"][district_id] = {"total": {}, "regions": {}}

            district = result["districts"][district_id]

            if region_id not in district["regions"]:
                district["regions"][region_id] = {"name": row.region_name, "stats": {}}

            # Обновляем статистику
            if type_name not in result["total"]:
                result["total"][type_name] = 0
            result["total"][type_name] += count

            if type_name not in district["total"]:
                district["total"][type_name] = 0
            district["total"][type_name] += count

            if type_name not in district["regions"][region_id]["stats"]:
                district["regions"][region_id]["stats"][type_name] = 0
            district["regions"][region_id]["stats"][type_name] += count

        # Формируем результат
        return self._format_results(result, districts_info)

    # USE
    @connection
    async def get_statistics_district_by_id(
        self, district_id: int, params: RequestBodySchema, session: AsyncSession
    ):

        start_date = (
            datetime.strptime(params.start_date, "%Y-%m-%d").date()
            if params.start_date
            else None
        )
        end_date = (
            datetime.strptime(params.end_date, "%Y-%m-%d").date()
            if params.end_date
            else None
        )
        query = """
            WITH type_counts_by_region AS (
                SELECT 
                    r.id AS region_id,
                    r.name AS region_name,
                    r.id_dist AS district_id,
                    t.name AS type_name,
                    COUNT(*) AS type_count
                FROM documents doc
                JOIN regions r ON doc.id_reg = r.id
                JOIN types t ON doc.id_type = t.id
                WHERE r.id_dist = :district_id
                {date_filter}
                {region_filter}
                GROUP BY r.id, r.name, r.id_dist, t.name
            ),
            region_stats AS (
                SELECT 
                    region_id,
                    region_name,
                    SUM(type_count) AS region_count,
                    JSON_AGG(
                        JSON_BUILD_OBJECT(
                            'name', type_name,
                            'count', type_count
                        )
                    ) AS stat
                FROM type_counts_by_region
                GROUP BY region_id, region_name
            ),
            district_type_stats AS (
                SELECT 
                    district_id,
                    type_name,
                    SUM(type_count) AS type_count
                FROM type_counts_by_region
                GROUP BY district_id, type_name
            ),
            district_stats AS (
                SELECT 
                    d.id AS district_id,
                    d.name AS district_name,
                    SUM(dts.type_count) AS total_count,
                    JSON_AGG(
                        JSON_BUILD_OBJECT(
                            'name', dts.type_name,
                            'count', dts.type_count
                        )
                    ) AS stat
                FROM district_type_stats dts
                JOIN districts d ON dts.district_id = d.id
                WHERE d.id = :district_id
                GROUP BY d.id, d.name
            )
            SELECT 
                JSON_BUILD_OBJECT(
                    'id', ds.district_id,
                    'name', ds.district_name,
                    'count', ds.total_count,
                    'stat', ds.stat,
                    'regions', (
                        SELECT JSON_AGG(
                            JSON_BUILD_OBJECT(
                                'id', rs.region_id,
                                'name', rs.region_name,
                                'count', rs.region_count,
                                'stat', rs.stat
                            )
                        )
                        FROM region_stats rs
                    )
                ) AS result
            FROM district_stats ds;
            """

        date_filter = (
            "AND doc.view_date BETWEEN :start_date AND :end_date"
            if start_date and end_date
            else ""
        )

        region_filter = "AND r.id = ANY(:region_ids)" if params.ids else ""
        query = query.format(date_filter=date_filter, region_filter=region_filter)
        result = await session.execute(
            text(query),
            {
                "district_id": district_id,
                "start_date": start_date,
                "end_date": end_date,
                "region_ids": params.ids,  # Передаём список как массив
            },
        )

        res = result.scalar_one_or_none()
        if res:
            return res
        else:
            return []
    @connection
    async def get_statistics_districts(
        self, params: RequestBodySchema, session: AsyncSession
    ):

        start_date = (
            datetime.strptime(params.start_date, "%Y-%m-%d").date()
            if params.start_date
            else None
        )
        end_date = (
            datetime.strptime(params.end_date, "%Y-%m-%d").date()
            if params.end_date
            else None
        )
        query = """
            WITH type_counts_by_region AS (
                SELECT 
                    r.id_dist AS district_id,
                    t.name AS type_name,
                    COUNT(*) AS type_count
                FROM documents doc
                JOIN regions r ON doc.id_reg = r.id
                JOIN types t ON doc.id_type = t.id
                WHERE 1=1
                {date_filter}
                {district_filter}
                GROUP BY r.id_dist, t.name
            ),
            district_type_stats AS (
                SELECT 
                    district_id,
                    type_name,
                    SUM(type_count) AS type_count
                FROM type_counts_by_region
                GROUP BY district_id, type_name
            ),
            district_stats AS (
                SELECT 
                    d.id AS district_id,
                    d.name AS district_name,
                    SUM(dts.type_count) AS total_count,
                    JSON_AGG(
                        JSON_BUILD_OBJECT(
                            'name', dts.type_name,
                            'count', dts.type_count
                        )
                    ) AS stat
                FROM district_type_stats dts
                JOIN districts d ON dts.district_id = d.id
                GROUP BY d.id, d.name
            ),
            overall_stats AS (
                SELECT 
                    SUM(dts.type_count) AS total_count,
                    JSON_AGG(
                        JSON_BUILD_OBJECT(
                            'name', dts.type_name,
                            'count', dts.type_count
                        )
                    ) AS stat
                FROM district_type_stats dts
            )
            SELECT 
                JSON_BUILD_OBJECT(
                    'name', 'Вся статистика',
                    'count', (SELECT total_count FROM overall_stats),
                    'stat', (SELECT stat FROM overall_stats),
                    'districts', JSON_AGG(
                        JSON_BUILD_OBJECT(
                            'id', ds.district_id,
                            'name', ds.district_name,
                            'count', ds.total_count,
                            'stat', ds.stat
                        )
                    )
                ) AS result
            FROM district_stats ds; 
        """

        date_filter = (
            "AND doc.view_date BETWEEN :start_date AND :end_date"
            if start_date and end_date
            else ""
        )
        district_filter = "AND r.id_dist = ANY(:district_ids)" if params.ids else ""
        query = query.format(date_filter=date_filter, district_filter=district_filter)

        result = await session.execute(
            text(query),
            {
                "district_ids": params.ids,
                "start_date": start_date,
                "end_date": end_date,
            },
        )

        res = result.scalar_one_or_none()
        if res:
            return res
        else:
            return []

    async def get_regions_in_district(
        self, district_id: int, params: RequestBodySchema
    ):
        """Получение статистики по регионам в конкретном округе"""

        # Получаем данные для одного округа
        regions_data, district_info = await self.get_regions_in_district_data(
            district_id, params
        )

        if not district_info:
            raise ResultIsEmptyError(f"Округ с ID {district_id} не найден")

        # Подготавливаем структуру результата
        district_total = {}
        regions = {}

        # Заполняем структуру данными
        for row in regions_data:
            region_id = row.region_id
            region_name = row.region_name
            type_name = row.type_name
            count = row.count

            # Инициализируем структуру, если еще не создана
            if region_id not in regions:
                regions[region_id] = {"name": region_name, "stats": {}}

            # Обновляем статистику
            if type_name not in district_total:
                district_total[type_name] = 0
            district_total[type_name] += count

            if type_name not in regions[region_id]["stats"]:
                regions[region_id]["stats"][type_name] = 0
            regions[region_id]["stats"][type_name] += count

        # Формируем список регионов
        region_list = []
        for region_id, region_data in regions.items():
            region_list.append(
                StatRegionSchema(
                    id=region_id,
                    name=region_data["name"],
                    count=sum(region_data["stats"].values()),
                    stat=[
                        StatBaseSchema(name=k, count=v)
                        for k, v in region_data["stats"].items()
                    ],
                )
            )

        # Создаем один округ
        district = StatDistrictSchema(
            id=district_id,
            name=district_info.name,
            count=sum(district_total.values()),
            stat=[StatBaseSchema(name=k, count=v) for k, v in district_total.items()],
            regions=region_list,
        )

        # Итоговый результат
        return StatAllSchema(
            name=f"Статистика по округу {district_info.name}",
            count=sum(district_total.values()),
            stat=[StatBaseSchema(name=k, count=v) for k, v in district_total.items()],
            districts=[district],
        )

    def _format_results(self, stat_data, districts_info):
        """Форматирование результатов для ответа API"""
        districts = []

        for district_id, district_stats in stat_data["districts"].items():
            if district_id not in districts_info:
                continue

            district_name = districts_info[district_id].name

            regions = []
            for region_id, region_data in district_stats["regions"].items():
                regions.append(
                    StatRegionSchema(
                        id=region_id,
                        name=region_data["name"],
                        count=sum(region_data["stats"].values()),
                        stat=[
                            StatBaseSchema(name=k, count=v)
                            for k, v in region_data["stats"].items()
                        ],
                    )
                )

            districts.append(
                StatDistrictSchema(
                    id=district_id,
                    name=district_name,
                    count=sum(district_stats["total"].values()),
                    stat=[
                        StatBaseSchema(name=k, count=v)
                        for k, v in district_stats["total"].items()
                    ],
                    regions=regions,
                )
            )

        return StatAllSchema(
            name="Вся статистика",
            count=sum(stat_data["total"].values()),
            stat=[
                StatBaseSchema(name=k, count=v) for k, v in stat_data["total"].items()
            ],
            districts=districts,
        )
