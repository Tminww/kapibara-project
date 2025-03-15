from abc import ABC, abstractmethod
from datetime import datetime

from models.act import ActEntity
from models.district import DistrictEntity
from models.document import DocumentEntity
from models.region import RegionEntity

from schemas.subjects import RegionInfoDTO, RegionsInDistrictDTO
from schemas.statistics import (
    RequestMaxMinBodySchema,
    StatRowSchema,
    StatBaseDTO,
    RequestBodySchema,
)
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
from database.setup import async_session_maker
from errors import ResultIsEmptyError


class SQLAlchemyRepository:

    async def get_definite_regions_in_district(
        self, parameters: RequestBodySchema, id_dist
    ):
        async with async_session_maker() as session:
            stmt = select(RegionEntity).filter(
                (parameters.regions is None or RegionEntity.id.in_(parameters.regions)),
                (RegionEntity.id_dist == id_dist),
            )
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                raise ResultIsEmptyError("Result is empty")

    async def get_stat_all(self, parameters: RequestBodySchema):
        async with async_session_maker() as session:
            start_date = (
                datetime.strptime(parameters.start_date, "%Y-%m-%d")
                if parameters.start_date is not None
                else None
            )
            end_date = (
                datetime.strptime(parameters.end_date, "%Y-%m-%d")
                if parameters.end_date is not None
                else None
            )

            stmt = (
                select(
                    ActEntity.name.label("name"),
                    func.count().label("count"),
                )
                .select_from(DocumentEntity)
                .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
                .join(ActEntity, DocumentEntity.id_act == ActEntity.id)
                .filter(
                    (
                        parameters.regions is None
                        or RegionEntity.id.in_(parameters.regions)
                    ),
                    (
                        parameters.start_date is None
                        and parameters.end_date is None
                        or DocumentEntity.view_date.between(start_date, end_date)
                    ),
                )
                .group_by(ActEntity.name)
                .order_by(ActEntity.name)
            )
            res = await session.execute(stmt)
            print(res)
            res = [StatBaseDTO(name=row.name, count=row.count) for row in res.all()]
            print(res)
            if res:
                return res
            else:
                print("get_stat_all")
                raise ResultIsEmptyError("Result is empty")

    async def get_stat_in_district(self, parameters: RequestBodySchema, id_dist):
        async with async_session_maker() as session:
            start_date = (
                datetime.strptime(parameters.start_date, "%Y-%m-%d")
                if parameters.start_date is not None
                else None
            )
            end_date = (
                datetime.strptime(parameters.end_date, "%Y-%m-%d")
                if parameters.end_date is not None
                else None
            )

            stmt = (
                select(
                    ActEntity.name.label("name"),
                    func.count().label("count"),
                )
                .select_from(DocumentEntity)
                .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
                .join(ActEntity, DocumentEntity.id_act == ActEntity.id)
                .filter(
                    (RegionEntity.id_dist == id_dist),
                    (
                        parameters.regions is None
                        or RegionEntity.id.in_(parameters.regions)
                    ),
                    (
                        parameters.start_date is None
                        and parameters.end_date is None
                        or DocumentEntity.view_date.between(start_date, end_date)
                    ),
                )
                .group_by(ActEntity.name)
                .order_by(ActEntity.name)
            )
            res = await session.execute(stmt)
            res = [StatBaseDTO(name=row.name, count=row.count) for row in res.all()]

            return res
            # if res:
            #     return res
            # else:
            #     raise ResultIsEmptyError("Result is empty")


    async def get_stat_in_districts(self, parameters: RequestBodySchema):
        async with async_session_maker() as session:
            start_date = (
                datetime.strptime(parameters.start_date, "%Y-%m-%d")
                if parameters.start_date is not None
                else None
            )
            end_date = (
                datetime.strptime(parameters.end_date, "%Y-%m-%d")
                if parameters.end_date is not None
                else None
            )

            stmt = (
                select(
                    ActEntity.name.label("name"),
                    func.count().label("count"),
                )
                .select_from(DocumentEntity)
                .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
                .join(ActEntity, DocumentEntity.id_act == ActEntity.id)
                .filter(
                    
                    (
                        parameters.regions is None
                        or RegionEntity.id_dist.in_(parameters.regions)
                    ),
                    (
                        parameters.start_date is None
                        and parameters.end_date is None
                        or DocumentEntity.view_date.between(start_date, end_date)
                    ),
                )
                .group_by(ActEntity.name)
                .order_by(ActEntity.name)
            )
            res = await session.execute(stmt)
            res = [StatBaseDTO(name=row.name, count=row.count) for row in res.all()]

            return res
            # if res:
            #     return res
            # else:
            #     raise ResultIsEmptyError("Result is empty")
    async def get_districts_by_regions(self, regions):
        async with async_session_maker() as session:
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

    async def get_districts(self, parameters: RequestBodySchema):
        async with async_session_maker() as session:
            stmt = select(DistrictEntity).filter(
                parameters.regions is None
                or DistrictEntity.id.in_(parameters.regions)
            )
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                print("get_districts")
                raise ResultIsEmptyError("Result is empty")

    async def get_regions_in_district(self, id_dist):
        async with async_session_maker() as session:
            stmt = select(RegionEntity).filter(RegionEntity.id_dist == id_dist)
            res = await session.execute(stmt)

            res = [RegionInfoDTO(name=row[0].name, id=row[0].id) for row in res.all()]

            if res:
                return res
            else:
                print("get_regions_in_district")
                raise ResultIsEmptyError("Result is empty")

    async def get_stat_in_region(self, parameters: RequestBodySchema, id_reg):
        async with async_session_maker() as session:
            start_date = (
                datetime.strptime(parameters.start_date, "%Y-%m-%d")
                if parameters.start_date is not None
                else None
            )
            end_date = (
                datetime.strptime(parameters.end_date, "%Y-%m-%d")
                if parameters.end_date is not None
                else None
            )

            stmt = (
                select(
                    ActEntity.name.label("name"),
                    func.count().label("count"),
                )
                .select_from(DocumentEntity)
                .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
                .join(ActEntity, DocumentEntity.id_act == ActEntity.id)
                .filter(
                    (RegionEntity.id == id_reg),
                    (
                        start_date is None
                        and end_date is None
                        or DocumentEntity.view_date.between(start_date, end_date)
                    ),
                )
                .group_by(ActEntity.name)
                .order_by(ActEntity.name)
            )
            res = await session.execute(stmt)
            res = [StatBaseDTO(name=row.name, count=row.count) for row in res.all()]

            # if res:
            #     return res
            # else:
            #     raise ResultIsEmptyError("Result is empty")
            return res

    async def get_publication_by_nomenclature(self, parameters):
        async with async_session_maker() as session:
            start_date = (
                datetime.strptime(parameters.start_date, "%Y-%m-%d")
                if parameters.start_date is not None
                else None
            )
            end_date = (
                datetime.strptime(parameters.end_date, "%Y-%m-%d")
                if parameters.end_date is not None
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

            print(query)
            res = await session.execute(query)

            return res.all()

    async def get_publication_by_years(self, limit: int):
        async with async_session_maker() as session:

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

            print(query)
            res = await session.execute(query)

            return res.all()

    async def get_publication_by_districts(self, parameters: RequestBodySchema):
        async with async_session_maker() as session:
            start_date = (
                datetime.strptime(parameters.start_date, "%Y-%m-%d")
                if parameters.start_date is not None
                else None
            )
            end_date = (
                datetime.strptime(parameters.end_date, "%Y-%m-%d")
                if parameters.end_date is not None
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

            print(query)
            res = await session.execute(query)

            return res.all()

    async def get_publication_by_regions(self, parameters: RequestMaxMinBodySchema):
        async with async_session_maker() as session:
            start_date = (
                datetime.strptime(parameters.start_date, "%Y-%m-%d")
                if parameters.start_date is not None
                else None
            )
            end_date = (
                datetime.strptime(parameters.end_date, "%Y-%m-%d")
                if parameters.end_date is not None
                else None
            )

            order_func = desc if parameters.sort == "max" else asc

            query = (
                select(
                    RegionEntity.name.label("name"),  # Выбираем имя региона
                    func.count(DocumentEntity.id).label(
                        "count"
                    ),  # Подсчитываем документы
                )
                .select_from(RegionEntity)  # Начинаем с таблицы region
                .outerjoin(
                    DocumentEntity,
                    (DocumentEntity.id_reg == RegionEntity.id)
                    & (
                        DocumentEntity.view_date.between(start_date, end_date)
                        if parameters.start_date is not None
                        and parameters.end_date is not None
                        else True
                    ),  # Условие по дате только внутри JOIN
                )
                .where(RegionEntity.code.like("region%"))  # Фильтр по code
                .group_by(RegionEntity.name)  # Группировка по имени региона
                .order_by(
                    order_func(func.count(DocumentEntity.id))
                )  # Сортировка по количеству документов
                .limit(parameters.limit)  # Ограничение до 10 строк
            )

            print(query)
            res = await session.execute(query)

            return res.all()

    async def get_publication_by_nomenclature_detail_president_and_government(
        self, parameters: RequestBodySchema
    ):
        async with async_session_maker() as session:
            start_date = (
                datetime.strptime(parameters.start_date, "%Y-%m-%d")
                if parameters.start_date is not None
                else None
            )
            end_date = (
                datetime.strptime(parameters.end_date, "%Y-%m-%d")
                if parameters.end_date is not None
                else None
            )

            # --- Часть 1: Запрос для актов президента ---
            # CTE для отфильтрованных документов президента
            filtered_documents_president = (
                select(DocumentEntity.id_act, DocumentEntity.id)
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
                    distinct(ActEntity.id).label("act_id"), ActEntity.name.label("name")
                )
                .join(DocumentEntity, ActEntity.id == DocumentEntity.id_act)
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
                    president_acts.c.act_id == filtered_documents_president.c.id_act,
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
                select(DocumentEntity.id_act, DocumentEntity.id)
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
                    distinct(ActEntity.id).label("act_id"), ActEntity.name.label("name")
                )
                .join(DocumentEntity, ActEntity.id == DocumentEntity.id_act)
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
                    government_acts.c.act_id == filtered_documents_government.c.id_act,
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

    async def get_publication_by_acts(self, parameters: RequestBodySchema):
        async with async_session_maker() as session:
            start_date = (
                datetime.strptime(parameters.start_date, "%Y-%m-%d")
                if parameters.start_date is not None
                else None
            )
            end_date = (
                datetime.strptime(parameters.end_date, "%Y-%m-%d")
                if parameters.end_date is not None
                else None
            )

            query = (
                select(
                    ActEntity.name.label("name"),
                    func.count(DocumentEntity.id).label("count"),
                )
                .select_from(ActEntity)
                .join(
                    DocumentEntity,
                    and_(
                        ActEntity.id == DocumentEntity.id_act,
                        (
                            DocumentEntity.view_date.between(start_date, end_date)
                            if start_date is not None and end_date is not None
                            else True
                        ),
                    ),
                )
                .group_by(ActEntity.name)
            )

            print(query)
            res = await session.execute(query)

            return res.all()
