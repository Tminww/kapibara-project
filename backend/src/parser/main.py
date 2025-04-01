import asyncio
from datetime import datetime
import json
from typing import List
import httpx
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, ProgrammingError
from tenacity import retry, stop_after_attempt, wait_fixed
from config import settings
from database import connection
from utils import parser_logger as logger
from models import TypeEntity, RegionEntity, DocumentEntity, DistrictEntity
from schemas import DocumentSchema


def get_regions() -> List[dict]:
    """Загружает данные регионов из JSON."""
    try:
        with open(f"{settings.BASE_DIR}/parser/mock/regions.json", "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Ошибка при загрузке regions.json: {e}")
        return []


def get_districts() -> List[dict]:
    """Загружает данные районов из JSON."""
    try:
        with open(f"{settings.BASE_DIR}/parser/mock/districts.json", "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Ошибка при загрузке districts.json: {e}")
        return []


def get_types() -> List[dict]:
    """Загружает данные типов из JSON."""
    try:
        with open(f"{settings.BASE_DIR}/parser/mock/types.json", "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Ошибка при загрузке types.json: {e}")
        return []


@retry(
    stop=stop_after_attempt(3), wait=wait_fixed(2)
)  # 3 попытки с интервалом 2 секунды
async def fetch(client, url):
    return await client.get(url)


def get_documents_by_block(code: str) -> str:
    return f"{settings.EXTERNAL_URL}/api/Documents?block={code}&PageSize=200&Index=1"


def get_documents_by_block_and_document_types(
    external_id: str, code: str, index: int
) -> str:
    return f"{settings.EXTERNAL_URL}/api/Documents?DocumentTypes={external_id}&block={code}&PageSize=200&Index={index}"


def get_document_types_by_block(code: str) -> str:
    return f"{settings.EXTERNAL_URL}/api/DocumentTypes?block={code}"


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
    documents: List[DocumentSchema],
    session: AsyncSession,
):
    """Вставляет записи в таблицу documents асинхронно с использованием Pydantic-схемы."""
    try:
        # Преобразуем в словари для вставки
        values = [d.model_dump() for d in documents]
        # logger.debug(f"Values to insert: {values}")

        # Вставка с обработкой конфликтов по eo_number
        stmt_insert = insert(DocumentEntity).values(values)

        stmt_on_conflict = stmt_insert.on_conflict_do_nothing(
            constraint="uq_documents_eo_number_id_reg",
            # set_=dict(
            #     complex_name=stmt_insert.excluded.complex_name,
            #     pages_count=stmt_insert.excluded.pages_count,
            #     view_date=stmt_insert.excluded.view_date,
            #     id_reg=stmt_insert.excluded.id_reg,
            #     id_type=stmt_insert.excluded.id_type,
            #     pdf_file_length=stmt_insert.excluded.pdf_file_length,
            #     name=stmt_insert.excluded.name,
            #     document_date=stmt_insert.excluded.document_date,
            #     signatory_authority_id=stmt_insert.excluded.signatory_authority_id,
            #     number=stmt_insert.excluded.number,
            #     title=stmt_insert.excluded.title,
            #     external_id=stmt_insert.excluded.external_id,
            #     date_of_publication=stmt_insert.excluded.date_of_publication,
            #     updated_at=func.now(),
            # ),
        )

        # Выполняем запрос и получаем количество вставленных строк
        result = await session.execute(stmt_on_conflict)
        await session.commit()

        inserted_count = result.rowcount
        if inserted_count == 0 and len(values) < 200:
            logger.warning(
                f"Документы не вставлены {inserted_count} из {len(values)}, Данные: {values}"
            )
        else:
            logger.debug(f"Успешно вставлено {inserted_count} из {len(values)}")
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

        return count
    except Exception as e:
        logger.error(
            f"Ошибка при подсчёте документов для региона {code} with type {external_id}: {e}"
        )
        return 0


async def get_document_api(region: dict, client: httpx.AsyncClient):

    code = region.get("code")
    region_name = region.get("short_name")
    logger.info(f"Регион {region_name} {code} начат")
    print(f"Регион {code} начат")

    # Запрос общего количества документов
    req_total_documents = await fetch(client, url=get_documents_by_block(code))

    # Проверка статуса ответа
    if req_total_documents.status_code != 200:
        logger.error(f"Ошибка при запросе: статус {req_total_documents.status_code}")
        return

    # Попытка парсинга JSON
    try:
        total_documents_data = req_total_documents.json()
    except ValueError as e:
        logger.error(f"Ошибка при парсинге JSON: {e}")
        return

    # Проверка, нужно ли обновлять данные
    if await get_total_documents(code=code) == total_documents_data.get(
        "itemsTotalCount"
    ):
        logger.info(f"Регион {region_name} {code} уже заполнен")
        print(f"Регион {code} уже заполнен")
        return

    # Запрос типов документов
    req_type = await fetch(client, url=get_document_types_by_block(code))

    # Проверка статуса ответа
    if req_type.status_code != 200:
        logger.error(
            f"Ошибка при запросе типов документов: статус {req_type.status_code}"
        )
        return

    # Попытка парсинга JSON
    try:
        types = req_type.json()
    except ValueError as e:
        logger.error(f"Ошибка при парсинге JSON типов документов: {e}")
        return

    # Обработка каждого типа документа
    for type in types:
        current_page = 1
        while True:
            # time.sleep(0.5)
            req = await fetch(
                client,
                url=get_documents_by_block_and_document_types(
                    external_id=type["id"], code=code, index=str(current_page)
                ),
            )

            # Проверка статуса ответа
            if req.status_code != 200:
                logger.error(f"Ошибка при запросе документов: статус {req.status_code}")
                break

            # Попытка парсинга JSON
            try:
                documents_data = req.json()
            except ValueError as e:
                logger.error(f"Ошибка при парсинге JSON документов: {e}")
                break

            # Проверка, нужно ли обновлять данные

            if current_page <= documents_data.get("pagesTotalCount", 0):

                id_reg = await get_id_reg(code=code)
                id_type = await get_id_type(external_id=type["id"])
                type_expected = documents_data.get("itemsTotalCount", 0)
                total_pages = documents_data.get("pagesTotalCount", 0)

                type_total = await get_total_documents_type(
                    code=code, external_id=type["id"]
                )
                if type_total == documents_data.get("itemsTotalCount"):
                    break

                logger.debug(
                    f"Type  {id_type}, page {current_page}/{total_pages}: DB={type_total}, API={type_expected}"
                )
                documents_for_insert = []
                for item in documents_data.get("items", []):

                    documents_for_insert.append(
                        DocumentSchema(
                            id=None,
                            eo_number=item.get("eoNumber"),
                            complex_name=item.get("complexName"),
                            pages_count=item.get("pagesCount"),
                            pdf_file_length=item.get("pdfFileLength"),
                            name=item.get("name"),
                            document_date=item.get("documentDate").split("T")[0],
                            signatory_authority_id=item.get("signatoryAuthorityId"),
                            # number=item.get("number"),
                            title=item.get("title"),
                            view_date=item.get("viewDate"),
                            external_id=item.get("id"),
                            id_reg=id_reg,  # Добавляем извне
                            id_type=id_type,  # Добавляем извне
                            date_of_publication=item.get("publishDateShort").split("T")[
                                0
                            ],
                            date_of_signing=None,  # Нет в JSON, оставляем None
                            updated_at=None,  # Нет в JSON, оставляем None или можно установить текущее время
                        )
                    )

                await insert_document(documents_for_insert)

                current_page += 1
            else:
                break

    logger.info(f"Регион {region_name} {code} закончен")
    print(f"Регион {code} закончен")


async def parse():
    """Основная функция парсинга."""
    logger.info("Начало парсинга")
    async with httpx.AsyncClient(
        proxy=settings.PROXY, timeout=httpx.Timeout(30.0)
    ) as client:
        types = get_types()
        districts = get_districts()
        regions = get_regions()

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
