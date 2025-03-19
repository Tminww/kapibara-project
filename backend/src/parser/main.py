import asyncio
from datetime import datetime
import json
from typing import List
import httpx
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, ProgrammingError

from config import settings
from database.setup import connection
from utils.logger import parser_logger as logger
from models import TypeEntity, RegionEntity, DocumentEntity, DistrictEntity
from schemas import DocumentSchema


@connection
async def insert_types(types: List[dict], session: AsyncSession):
    """Вставляет записи в таблицу types асинхронно."""
    try:
        values = [
            {
                "name": t.get("name"),
                "weight": int(t.get("weight")),
                "external_id": t.get("id"),
            }
            for t in types
        ]
        stmt_insert = insert(TypeEntity).values(values)
        stmt_on_conflict = stmt_insert.on_conflict_do_update(
            constraint="uq_types_external_id",
            set_=dict(
                name=stmt_insert.excluded.name,
                weight=stmt_insert.excluded.weight,
                external_id=stmt_insert.excluded.external_id,
            ),
        )
        result = await session.execute(stmt_on_conflict)
        await session.commit()
        inserted_count = result.rowcount if result.rowcount is not None else len(values)

        logger.info(f"Successfully inserted {inserted_count} types")
        return inserted_count > 0
    except ProgrammingError as e:
        logger.error(f"Ошибка структуры таблицы types: {e}")
        return False
    except IntegrityError as e:
        logger.error(f"Нарушение целостности данных при вставке в types: {e}")
        return False
    except Exception as e:
        logger.error(f"Неизвестная ошибка при вставке в types: {e}")
        return False


@connection
async def insert_region(regions: List[dict], session: AsyncSession):
    try:
        values = [
            {
                "id_dist": r.get("id_dist"),
                "name": r.get("name"),
                "short_name": r.get("short_name"),
                "external_id": r.get("external_id"),
                "code": r.get("code"),
            }
            for r in regions
        ]
        stmt_insert = insert(RegionEntity).values(values)
        stmt_on_conflict = stmt_insert.on_conflict_do_update(
            constraint="uq_regions_external_id",
            set_=dict(
                name=stmt_insert.excluded.name,
                short_name=stmt_insert.excluded.short_name,
                external_id=stmt_insert.excluded.external_id,
                code=stmt_insert.excluded.code,
                id_dist=stmt_insert.excluded.id_dist,
            ),
        )
        result = await session.execute(stmt_on_conflict)
        await session.commit()
        inserted_count = result.rowcount if result.rowcount is not None else len(values)

        logger.info(f"Successfully inserted {inserted_count} regions")
        return inserted_count > 0
    except ProgrammingError as e:
        logger.warning(f"Отсутствует уникальный индекс: {e}")
        return False
    except IntegrityError as e:
        logger.error(f"Нарушение целостности данных: {e}")
        return False
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        return False


@connection
async def insert_districts(districts: List[dict], session: AsyncSession):
    try:
        values = [
            {
                "id": d.get("id"),
                "name": d.get("name"),
                "short_name": d.get("short_name"),
                "full_name": d.get("full_name"),
            }
            for d in districts
        ]
        stmt_insert = insert(DistrictEntity).values(values)
        stmt_on_conflict = stmt_insert.on_conflict_do_update(
            constraint="districts_pkey",
            set_=dict(
                name=stmt_insert.excluded.name,
                short_name=stmt_insert.excluded.short_name,
                full_name=stmt_insert.excluded.full_name,
            ),
        )
        result = await session.execute(stmt_on_conflict)
        await session.commit()
        inserted_count = result.rowcount if result.rowcount is not None else len(values)
        logger.info(f"Successfully inserted {inserted_count} districts")
        return inserted_count > 0
    except ProgrammingError as e:
        logger.warning(f"Отсутствует уникальный индекс: {e}")
        return False
    except IntegrityError as e:
        logger.error(f"Нарушение целостности данных: {e}")
        return False
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        return False


@connection
async def get_id_reg(code: str, session: AsyncSession) -> int:
    """Получает ID региона по коду."""
    try:
        stmt = select(RegionEntity.id).where(RegionEntity.code == code)
        result = await session.execute(stmt)
        id_reg = result.scalar_one_or_none()
        if id_reg is None:
            logger.warning(f"Region with code {code} not found, attempting to insert")
            success = await insert_region([{"name": f"Region {code}", "code": code}])
            if success:
                result = await session.execute(stmt)
                id_reg = result.scalar_one_or_none()
                if id_reg is not None:
                    return id_reg
            raise ValueError(
                f"Region with code {code} not found after insertion attempt"
            )
        return id_reg
    except Exception as e:
        logger.error(f"Ошибка при получении ID региона для кода {code}: {e}")
        return -1


@connection
async def get_id_type(external_id: str, session: AsyncSession) -> int:
    """Получает ID акта по external_id."""
    try:
        stmt = select(TypeEntity.id).where(TypeEntity.external_id == external_id)
        result = await session.execute(stmt)
        id_type = result.scalar_one_or_none()
        if id_type is None:
            raise ValueError(f"Act with external_id {external_id} not found")
        return id_type
    except Exception as e:
        logger.error(f"Ошибка при получении ID акта для external_id {external_id}: {e}")
        return -1


@connection
async def insert_document(
    complex_names: List[str],
    eo_numbers: List[str],
    pages_counts: List[int],
    view_dates: List[str],
    id_regs: List[int],
    id_types: List[int],
    session: AsyncSession,
):
    """Вставляет записи в таблицу documents асинхронно с использованием Pydantic-схемы."""
    try:
        # Проверяем существующие eo_number в базе
        existing_stmt = select(DocumentEntity.eo_number).where(
            DocumentEntity.eo_number.in_(eo_numbers)
        )
        result = await session.execute(existing_stmt)
        existing_eo_numbers = set(result.scalars().all())
        logger.debug(f"Existing eo_numbers in DB: {existing_eo_numbers}")

        # Фильтруем только новые документы
        new_documents = [
            DocumentSchema(
                complex_name=cn,
                eo_number=en,
                pages_count=pc,
                view_date=vd,
                id_reg=ir,
                id_type=ia,
            )
            for cn, en, pc, vd, ir, ia in zip(
                complex_names, eo_numbers, pages_counts, view_dates, id_regs, id_types
            )
            if en not in existing_eo_numbers  # Пропускаем существующие
        ]

        if not new_documents:
            logger.info("No new documents to insert")
            return

        # Преобразуем в словари для вставки
        values = [doc.model_dump(exclude_none=True) for doc in new_documents]
        logger.debug(f"Values to insert: {values}")

        # Вставка с обработкой конфликтов по eo_number
        stmt = (
            insert(DocumentEntity)
            .values(values)
            .on_conflict_do_nothing(
                index_elements=["eo_number"]  # Уникальность по eo_number
            )
        )

        # Выполняем запрос и получаем количество вставленных строк
        result = await session.execute(stmt)
        await session.commit()

        inserted_count = result.rowcount
        logger.info(f"Successfully inserted {inserted_count} new documents")
    except ProgrammingError as e:
        logger.error(f"Ошибка структуры таблицы documents: {e}")
        await session.rollback()
        raise
    except IntegrityError as e:
        logger.error(f"Нарушение целостности данных при вставке в documents: {e}")
        await session.rollback()
        raise
    except Exception as e:
        logger.error(f"Неизвестная ошибка при вставке в documents: {e}")
        await session.rollback()
        raise


@connection
async def get_total_documents(code: str, session: AsyncSession) -> int:
    """Подсчитывает общее количество документов для региона."""
    try:
        id_reg = await get_id_reg(code)
        if id_reg == -1:
            return 0
        stmt = (
            select(func.count())
            .select_from(DocumentEntity)
            .where(DocumentEntity.id_reg == id_reg)
        )
        result = await session.execute(stmt)
        count = result.scalar()
        logger.info(f"Total documents for region {code}: {count}")
        return count
    except Exception as e:
        logger.error(f"Ошибка при подсчёте документов для региона {code}: {e}")
        return 0


@connection
async def get_total_documents_type(
    code: str, external_id: str, session: AsyncSession
) -> int:
    """Подсчитывает количество документов определённого типа для региона."""
    try:
        id_reg = await get_id_reg(code)
        id_type = await get_id_type(external_id)
        if id_reg == -1 or id_type == -1:
            return 0
        stmt = (
            select(func.count())
            .select_from(DocumentEntity)
            .where(DocumentEntity.id_reg == id_reg, DocumentEntity.id_type == id_type)
        )
        result = await session.execute(stmt)
        count = result.scalar()
        logger.info(
            f"Total documents for region {code} with type {external_id}: {count}"
        )
        return count
    except Exception as e:
        logger.error(
            f"Ошибка при подсчёте документов для региона {code} with type {external_id}: {e}"
        )
        return 0


def regions_data() -> List[dict]:
    """Загружает данные регионов из JSON."""
    try:
        with open(f"{settings.BASE_DIR}/parser/mock/regions.json", "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Ошибка при загрузке regions.json: {e}")
        return []


def districts_data() -> List[dict]:
    """Загружает данные районов из JSON."""
    try:
        with open(f"{settings.BASE_DIR}/parser/mock/districts.json", "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Ошибка при загрузке districts.json: {e}")
        return []


def types_data() -> List[dict]:
    """Загружает данные типов из JSON."""
    try:
        with open(f"{settings.BASE_DIR}/parser/mock/types.json", "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Ошибка при загрузке types.json: {e}")
        return []


def get_documents_on_page(code: str) -> str:
    return f"{settings.EXTERNAL_URL}/api/Documents?block={code}&PageSize=200&Index=1"


def get_documents_on_page_type(external_id: str, code: str, index: int) -> str:
    return f"{settings.EXTERNAL_URL}/api/Documents?DocumentTypes={external_id}&block={code}&PageSize=200&Index={index}"


def get_subjects() -> str:
    return f"{settings.EXTERNAL_URL}/api/PublicBlocks/?parent=subjects"


def get_type_all() -> str:
    return f"{settings.EXTERNAL_URL}/api/DocumentTypes"


def get_type_in_subject(code: str) -> str:
    return f"{settings.EXTERNAL_URL}/api/DocumentTypes?block={code}"


async def get_document_api(region: dict, client: httpx.AsyncClient):
    """Асинхронно получает и парсит документы для региона."""
    code = region.get("code")
    region_name = region.get("short_name")
    logger.info(f"Объект {region_name}, {code} начат")
    print(f"Объект {region_name}, {code} начат")

    try:
        resp = await client.get(get_documents_on_page(code))
        resp.raise_for_status()
        total_documents_data = resp.json()
    except httpx.RequestError as e:
        logger.error(
            f"Ошибка запроса документов для региона {region_name}, {code}: {e}"
        )
        return
    except Exception as e:
        logger.error(
            f"Неизвестная ошибка при запросе документов для региона {region_name}, {code}: {e}"
        )
        return

    total_docs = await get_total_documents(code)
    total_expected = total_documents_data.get("itemsTotalCount", 0)
    if total_docs >= total_expected:
        logger.info(
            f"Регион {region_name}, {code} уже заполнен (DB: {total_docs}, API: {total_expected})"
        )
        print(f"Регион {region_name}, {code} уже заполнен")
        return

    try:
        resp = await client.get(get_type_in_subject(code))
        resp.raise_for_status()
        types: List[dict] = resp.json()
    except httpx.RequestError as e:
        logger.error(
            f"Ошибка запроса типов документов для региона {region_name}, {code}: {e}"
        )
        return
    except Exception as e:
        logger.error(
            f"Неизвестная ошибка при запросе типов документов для региона {region_name}, {code}: {e}"
        )
        return

    for type_ in types:
        current_page = 1
        type_id = type_.get("id")
        while True:
            await asyncio.sleep(0.5)
            url = get_documents_on_page_type(type_id, code, current_page)
            try:
                resp = await client.get(url)
                resp.raise_for_status()
                documents_data: dict = resp.json()
            except httpx.RequestError as e:
                logger.error(
                    f"Ошибка запроса документов для региона {region_name}, {code}, {type_.get('name')} {type_id}: {e}"
                )
                break
            except Exception as e:
                logger.error(
                    f"Неизвестная ошибка при запроса документов для региона {region_name}, {code}, {type_.get('name')} {type_id}: {e}"
                )
                break

            type_total = await get_total_documents_type(code, type_id)
            type_expected = documents_data.get("itemsTotalCount", 0)
            if type_total >= type_expected:
                logger.debug(
                    f"Type {type_id} already fully inserted (DB: {type_total}, API: {type_expected})"
                )
                break

            if current_page <= documents_data.get("pagesTotalCount", 0):
                complex_names = []
                eo_numbers = []
                pages_counts = []
                view_dates = []
                id_regs = []
                id_types = []
                id_reg = await get_id_reg(code)
                id_type = await get_id_type(type_id)

                if id_reg == -1 or id_type == -1:
                    logger.error(
                        f"Пропуск вставки документов для региона {code}, type {type_id} из-за ошибки ID"
                    )
                    break

                for item in documents_data.get("items", []):
                    complex_names.append(item.get("complexName"))
                    eo_numbers.append(item.get("eoNumber"))
                    pages_counts.append(item.get("pagesCount"))
                    view_dates.append(item.get("viewDate"))
                    id_regs.append(id_reg)
                    id_types.append(id_type)

                await insert_document(
                    complex_names,
                    eo_numbers,
                    pages_counts,
                    view_dates,
                    id_regs,
                    id_types,
                )

                # Проверяем общее количество после вставки
                new_total = await get_total_documents_type(code, type_id)
                if new_total >= type_expected:
                    logger.debug(
                        f"Type {type_id} fully inserted after update (DB: {new_total}, API: {type_expected})"
                    )
                    break

                current_page += 1
            else:
                break

    logger.info(f"Регион {code} закончен")
    print(f"Регион {code} закончен")


async def parse():
    """Основная функция парсинга."""
    logger.info("Начало парсинга")
    async with httpx.AsyncClient(proxy=settings.PROXY) as client:
        types = types_data()
        districts = districts_data()
        regions = regions_data()

        if not regions or not districts or not types:
            logger.error("Не удалось загрузить начальные данные, завершение парсинга")
            return

        await insert_types(types)
        await insert_districts(districts)
        await insert_region(regions)

        for region in regions:
            await get_document_api(region, client)


if __name__ == "__main__":
    asyncio.run(parse())
