from datetime import datetime
from sqlalchemy import (
    asc,
    desc,
    distinct,
    insert,
    select,
    func,
    text,
    and_,
    or_,
    case,
    union,
)
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
    TypeEntity,
    DistrictEntity,
    DocumentEntity,
    RegionEntity,
)

from schemas import (
    RequestMaxMinBodySchema,
    RequestBodySchema,
)
from database import connection
from errors import ResultIsEmptyError


class DashboardRepository:

    @connection
    async def get_publication_by_nomenclature(self, params, session: AsyncSession):

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
        region_case = case(
            (RegionEntity.code.startswith("region"), "ОГВ Субъектов РФ"),
            else_=RegionEntity.name,
        ).label("name")

        # Базовый запрос
        query = (
            select(region_case, func.count().label("count"))
            .select_from(DocumentEntity)
            .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
        )

        # Условия фильтрации по дате
        date_filter = (
            start_date is None
            and end_date is None
            or DocumentEntity.view_date.between(start_date, end_date)
        )
        query = query.filter(date_filter)

        # Группировка
        query = query.group_by(region_case)

        res = await session.execute(query)

        return res.all()

    @connection
    async def get_publication_by_years(self, limit: int, session: AsyncSession):

        year_expr = func.date_part("year", DocumentEntity.view_date).label("name")
        query = (
            select(year_expr, func.count().label("count"))
            .where(
                DocumentEntity.view_date
                >= func.current_date() - text(f"INTERVAL '{limit} years'")
            )
            .group_by(year_expr)
            .order_by("name")
        )

        res = await session.execute(query)

        return res.all()

    @connection
    async def get_publication_by_districts(
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
        query = (
            select(
                DistrictEntity.name.label("name"),
                func.count(DocumentEntity.id).label("count"),
            )
            .select_from(DocumentEntity)  # Указываем начальную таблицу
            .join(
                RegionEntity, DocumentEntity.id_reg == RegionEntity.id
            )  # Присоединяем Region
            .join(
                DistrictEntity, RegionEntity.id_dist == DistrictEntity.id
            )  # Присоединяем District
            .group_by(DistrictEntity.name)  # Группируем по имени округа
            .order_by(DistrictEntity.name.asc())  # Сортируем по имени
        )

        # Условия фильтрации по дате
        date_filter = (
            start_date is None
            and end_date is None
            or DocumentEntity.view_date.between(start_date, end_date)
        )
        query = query.filter(date_filter)

        res = await session.execute(query)

        return res.all()

    @connection
    async def get_publication_by_regions(
        self, params: RequestMaxMinBodySchema, session: AsyncSession
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

        order_func = desc if params.sort == "max" else asc

        query = (
            select(
                RegionEntity.name.label("name"),  # Выбираем имя региона
                func.count(DocumentEntity.id).label("count"),  # Подсчитываем документы
            )
            .select_from(RegionEntity)  # Начинаем с таблицы region
            .outerjoin(
                DocumentEntity,
                (DocumentEntity.id_reg == RegionEntity.id)
                & (
                    DocumentEntity.view_date.between(start_date, end_date)
                    if start_date is not None and end_date is not None
                    else True
                ),  # Условие по дате только внутри JOIN
            )
            .where(RegionEntity.code.like("region%"))  # Фильтр по code
            .group_by(RegionEntity.name)  # Группировка по имени региона
            .order_by(
                order_func(func.count(DocumentEntity.id))
            )  # Сортировка по количеству документов
            .limit(params.limit)  # Ограничение до 10 строк
        )

        res = await session.execute(query)

        return res.all()

    @connection
    async def get_publication_by_nomenclature_detail_president_and_government(
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
        # --- Часть 1: Запрос для актов президента ---
        # CTE для отфильтрованных документов президента
        filtered_documents_president = (
            select(DocumentEntity.id_type, DocumentEntity.id)
            .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
            .where(
                and_(
                    RegionEntity.code == "president",
                    (
                        DocumentEntity.view_date.between(start_date, end_date)
                        if start_date is not None and end_date is not None
                        else True
                    ),
                )
            )
            .cte("filtered_documents_president")
        )

        # CTE для актов президента
        president_acts = (
            select(
                distinct(TypeEntity.id).label("act_id"),
                TypeEntity.name.label("name"),
            )
            .join(DocumentEntity, TypeEntity.id == DocumentEntity.id_type)
            .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
            .where(RegionEntity.code == "president")
            .cte("president_acts")
        )

        # Основной запрос для президента
        president_query = (
            select(
                case(
                    (
                        president_acts.c.name == "Указ",
                        "Указ Президента Российской Федерации",
                    ),
                    (
                        president_acts.c.name == "Распоряжение",
                        "Распоряжение Президента Российской Федерации",
                    ),
                    (
                        president_acts.c.name == "Приказ",
                        "Приказ Президента Российской Федерации",
                    ),
                    else_=president_acts.c.name,
                ).label("name"),
                func.count(filtered_documents_president.c.id).label("count"),
            )
            .select_from(president_acts)
            .outerjoin(
                filtered_documents_president,
                president_acts.c.act_id == filtered_documents_president.c.id_type,
            )
            .group_by(
                president_acts.c.name,
                case(
                    (
                        president_acts.c.name == "Указ",
                        "Указ Президента Российской Федерации",
                    ),
                    (
                        president_acts.c.name == "Распоряжение",
                        "Распоряжение Президента Российской Федерации",
                    ),
                    (
                        president_acts.c.name == "Приказ",
                        "Приказ Президента Российской Федерации",
                    ),
                    else_=president_acts.c.name,
                ),
            )
            .order_by(func.count(filtered_documents_president.c.id).asc())
        )

        # --- Часть 2: Запрос для актов правительства ---
        # CTE для отфильтрованных документов правительства
        filtered_documents_government = (
            select(DocumentEntity.id_type, DocumentEntity.id)
            .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
            .where(
                and_(
                    RegionEntity.code == "government",
                    (
                        DocumentEntity.view_date.between(start_date, end_date)
                        if start_date is not None and end_date is not None
                        else True
                    ),
                )
            )
            .cte("filtered_documents_government")
        )

        # CTE для актов правительства
        government_acts = (
            select(
                distinct(TypeEntity.id).label("act_id"),
                TypeEntity.name.label("name"),
            )
            .join(DocumentEntity, TypeEntity.id == DocumentEntity.id_type)
            .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
            .where(RegionEntity.code == "government")
            .cte("government_acts")
        )

        # Основной запрос для правительства
        government_query = (
            select(
                case(
                    (
                        government_acts.c.name == "Постановление",
                        "Постановление Правительства Российской Федерации",
                    ),
                    (
                        government_acts.c.name == "Распоряжение",
                        "Распоряжение Правительства Российской Федерации",
                    ),
                    else_=government_acts.c.name,
                ).label("name"),
                func.count(filtered_documents_government.c.id).label("count"),
            )
            .select_from(government_acts)
            .outerjoin(
                filtered_documents_government,
                government_acts.c.act_id == filtered_documents_government.c.id_type,
            )
            .group_by(
                government_acts.c.name,
                case(
                    (
                        government_acts.c.name == "Постановление",
                        "Постановление Правительства Российской Федерации",
                    ),
                    (
                        government_acts.c.name == "Распоряжение",
                        "Распоряжение Правительства Российской Федерации",
                    ),
                    else_=government_acts.c.name,
                ),
            )
            .order_by(func.count(filtered_documents_government.c.id).asc())
        )

        # --- Часть 3: Запрос для регионов ---
        # CTE для отфильтрованных документов регионов
        filtered_documents_regions = (
            select(DocumentEntity.id_reg, DocumentEntity.id)
            .where(
                DocumentEntity.view_date.between(start_date, end_date)
                if start_date is not None and end_date is not None
                else True
            )
            .cte("filtered_documents_regions")
        )

        # CTE для регионов
        filtered_regions = (
            select(RegionEntity.id, RegionEntity.name, RegionEntity.code)
            .where(RegionEntity.code.notin_(["president", "government"]))
            .cte("filtered_regions")
        )

        # Основной запрос для регионов
        region_case = case(
            (filtered_regions.c.code.like("region%"), "ОГВ Субъектов РФ"),
            else_=filtered_regions.c.name,
        ).label("name")

        regions_query = (
            select(
                region_case,
                func.count(filtered_documents_regions.c.id).label("count"),
            )
            .select_from(filtered_regions)
            .outerjoin(
                filtered_documents_regions,
                filtered_documents_regions.c.id_reg == filtered_regions.c.id,
            )
            .group_by(region_case)
            .order_by("name")
        )

        # --- Объединение всех запросов ---
        combined_query = union(president_query, government_query, regions_query)
        print(combined_query)
        # --- Выполнение запроса и возврат результата ---
        result = await session.execute(combined_query)

        return result.all()

    @connection
    async def get_publication_by_types(
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
        query = (
            select(
                TypeEntity.name.label("name"),
                func.count(DocumentEntity.id).label("count"),
            )
            .select_from(TypeEntity)
            .join(
                DocumentEntity,
                and_(
                    TypeEntity.id == DocumentEntity.id_type,
                    (
                        DocumentEntity.view_date.between(start_date, end_date)
                        if start_date is not None and end_date is not None
                        else True
                    ),
                ),
            )
            .group_by(TypeEntity.name)
        )

        res = await session.execute(query)

        return res.all()
