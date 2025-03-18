import asyncio
from datetime import datetime
import json
from typing import List, Tuple
import httpx
from sqlalchemy import func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, ProgrammingError

from config import settings
from database.setup import get_async_session, connection
from utils.logger import parser_logger as logger
from models import ActEntity, RegionEntity, DocumentEntity

PROXY = "http://10.0.0.1:3128"


@connection
async def insert_act(name_npaId: List[Tuple[str, str]], session: AsyncSession):
    """Вставляет записи в таблицу acts асинхронно."""
    try:
        values = [{"name": name, "npa_id": npa_id} for name, npa_id in name_npaId]
        stmt = (
            insert(ActEntity)
            .values(values)
            .on_conflict_do_nothing(index_elements=["name", "npa_id"])
        )
        await session.execute(stmt)
        await session.commit()
        logger.info(f"Successfully inserted {len(values)} acts")
    except ProgrammingError as e:
        logger.error(f"Ошибка структуры таблицы acts: {e}")
    except IntegrityError as e:
        logger.error(f"Нарушение целостности данных при вставке в acts: {e}")
    except Exception as e:
        logger.error(f"Неизвестная ошибка при вставке в acts: {e}")


@connection
async def insert_region(name_code: List[Tuple[str, str]], session: AsyncSession):
    """Вставляет записи в таблицу regions асинхронно."""
    try:
        values = [{"name": name, "code": code} for name, code in name_code]
        stmt = (
            insert(RegionEntity)
            .values(values)
            .on_conflict_do_nothing(index_elements=["name", "code"])
        )
        result = await session.execute(stmt)
        await session.commit()
        inserted_count = result.rowcount if result.rowcount is not None else len(values)
        logger.info(f"Successfully inserted {inserted_count} regions")
        return inserted_count > 0  # Возвращаем True, если вставка успешна
    except ProgrammingError as e:
        logger.warning(
            f"Отсутствует уникальный индекс на name, code в таблице regions: {e}"
        )
        # Пробуем вставить без ON CONFLICT
        try:
            stmt = insert(RegionEntity).values(values)
            result = await session.execute(stmt)
            await session.commit()
            inserted_count = (
                result.rowcount if result.rowcount is not None else len(values)
            )
            logger.info(f"Inserted {inserted_count} regions without conflict handling")
            return inserted_count > 0
        except Exception as e2:
            logger.error(f"Не удалось вставить регионы даже без ON CONFLICT: {e2}")
            return False
    except IntegrityError as e:
        logger.error(f"Нарушение целостности данных при вставке в regions: {e}")
        return False
    except Exception as e:
        logger.error(f"Неизвестная ошибка при вставке в regions: {e}")
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
            # Пробуем вставить регион
            success = await insert_region([(f"Region {code}", code)])
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
async def get_id_act(npa_id: str, session: AsyncSession) -> int:
    """Получает ID акта по npa_id."""
    try:
        stmt = select(ActEntity.id).where(ActEntity.npa_id == npa_id)
        result = await session.execute(stmt)
        id_act = result.scalar_one_or_none()
        if id_act is None:
            raise ValueError(f"Act with npa_id {npa_id} not found")
        return id_act
    except Exception as e:
        logger.error(f"Ошибка при получении ID акта для npa_id {npa_id}: {e}")
        return -1


@connection
async def update_region(subjects_data: List[dict], session: AsyncSession):
    """Обновляет таблицу regions с id_dist."""
    try:
        for row in subjects_data:
            stmt = (
                update(RegionEntity)
                .where(RegionEntity.name == row["name"])
                .values(id_dist=row.get("id_dist"))
            )
            await session.execute(stmt)
        await session.commit()
        logger.info(f"Updated {len(subjects_data)} regions")
    except Exception as e:
        logger.error(f"Ошибка при обновлении regions: {e}")


@connection
async def insert_document(
    complex_names: List[str],
    eo_numbers: List[str],
    pages_counts: List[int],
    view_dates: List[str],
    id_regs: List[int],
    id_acts: List[int],
    session: AsyncSession,
):
    """Вставляет записи в таблицу documents асинхронно."""
    try:
        values = [
            {
                "complex_name": cn,
                "id_act": ia,
                "eo_number": en,
                "view_date": vd,
                "pages_count": pc,
                "id_reg": ir,
            }
            for cn, ia, en, vd, pc, ir in zip(
                complex_names, id_acts, eo_numbers, view_dates, pages_counts, id_regs
            )
        ]
        stmt = (
            insert(DocumentEntity)
            .values(values)
            .on_conflict_do_nothing(index_elements=["id", "eo_number"])
        )
        await session.execute(stmt)
        await session.commit()
        logger.info(f"Successfully inserted {len(values)} documents")
    except ProgrammingError as e:
        logger.error(f"Ошибка структуры таблицы documents: {e}")
    except IntegrityError as e:
        logger.error(f"Нарушение целостности данных при вставке в documents: {e}")
    except Exception as e:
        logger.error(f"Неизвестная ошибка при вставке в documents: {e}")


@connection
async def get_total_documents(code: str, session: AsyncSession) -> int:
    """Подсчитывает общее количество документов для региона."""
    try:
        id_reg = await get_id_reg(code)  # Убрана явная передача session
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
    code: str, npa_id: str, session: AsyncSession
) -> int:
    """Подсчитывает количество документов определённого типа для региона."""
    try:
        id_reg = await get_id_reg(code)  # Убрана явная передача session
        id_act = await get_id_act(npa_id)  # Убрана явная передача session
        if id_reg == -1 or id_act == -1:
            return 0
        stmt = (
            select(func.count())
            .select_from(DocumentEntity)
            .where(DocumentEntity.id_reg == id_reg, DocumentEntity.id_act == id_act)
        )
        result = await session.execute(stmt)
        count = result.scalar()
        logger.info(f"Total documents for region {code} and npa_id {npa_id}: {count}")
        return count
    except Exception as e:
        logger.error(
            f"Ошибка при подсчёте документов для региона {code} и npa_id {npa_id}: {e}"
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


def get_documents_on_page(code: str) -> str:
    return f"{settings.EXTERNAL_URL}/api/Documents?block={code}&PageSize=200&Index=1"


def get_documents_on_page_type(npa_id: str, code: str, index: int) -> str:
    return f"{settings.EXTERNAL_URL}/api/Documents?DocumentTypes={npa_id}&block={code}&PageSize=200&Index={index}"


def get_subjects() -> str:
    return f"{settings.EXTERNAL_URL}/api/PublicBlocks/?parent=subjects"


def get_type_all() -> str:
    return f"{settings.EXTERNAL_URL}/api/DocumentTypes"


def get_type_in_subject(code: str) -> str:
    return f"{settings.EXTERNAL_URL}/api/DocumentTypes?block={code}"


async def get_document_api(code: str, client: httpx.AsyncClient):
    """Асинхронно получает и парсит документы для региона."""
    logger.info(f"Регион {code} начат")
    print(f"Регион {code} начат")

    try:
        resp = await client.get(get_documents_on_page(code))
        resp.raise_for_status()
        total_documents_data = resp.json()
    except httpx.RequestError as e:
        logger.error(f"Ошибка запроса документов для региона {code}: {e}")
        return
    except Exception as e:
        logger.error(
            f"Неизвестная ошибка при запросе документов для региона {code}: {e}"
        )
        return

    total_docs = await get_total_documents(code)
    if total_docs == total_documents_data.get("itemsTotalCount"):
        logger.info(f"Регион {code} уже заполнен")
        print(f"Регион {code} уже заполнен")
        return

    try:
        resp = await client.get(get_type_in_subject(code))
        resp.raise_for_status()
        type_data = resp.json()
    except httpx.RequestError as e:
        logger.error(f"Ошибка запроса типов документов для региона {code}: {e}")
        return
    except Exception as e:
        logger.error(
            f"Неизвестная ошибка при запросе типов документов для региона {code}: {e}"
        )
        return

    for npa in type_data:
        current_page = 1
        while True:
            await asyncio.sleep(0.5)
            url = get_documents_on_page_type(npa["id"], code, current_page)
            try:
                resp = await client.get(url)
                resp.raise_for_status()
                documents_data = resp.json()
            except httpx.RequestError as e:
                logger.error(
                    f"Ошибка запроса документов для региона {code}, npa_id {npa['id']}: {e}"
                )
                break
            except Exception as e:
                logger.error(
                    f"Неизвестная ошибка при запросе документов для региона {code}, npa_id {npa['id']}: {e}"
                )
                break

            if await get_total_documents_type(code, npa["id"]) == documents_data.get(
                "itemsTotalCount"
            ):
                break

            if current_page <= documents_data.get("pagesTotalCount", 0):
                complex_names = []
                eo_numbers = []
                pages_counts = []
                view_dates = []
                id_regs = []
                id_acts = []
                id_reg = await get_id_reg(code)
                id_act = await get_id_act(npa["id"])

                if id_reg == -1 or id_act == -1:
                    logger.error(
                        f"Пропуск вставки документов для региона {code}, npa_id {npa['id']} из-за ошибки ID"
                    )
                    break

                for item in documents_data.get("items", []):
                    try:
                        complex_names.append(item.get("complexName"))
                        eo_numbers.append(item.get("eoNumber"))
                        pages_counts.append(item.get("pagesCount"))
                        view_dates.append(
                            datetime.strptime(
                                item.get("viewDate"), "%d.%m.%Y"
                            ).strftime("%Y-%m-%d")
                        )
                        id_regs.append(id_reg)
                        id_acts.append(id_act)
                    except ValueError as e:
                        logger.error(
                            f"Ошибка формата даты в документе для региона {code}: {e}"
                        )
                        continue

                await insert_document(
                    complex_names,
                    eo_numbers,
                    pages_counts,
                    view_dates,
                    id_regs,
                    id_acts,
                )
                current_page += 1
            else:
                break

    logger.info(f"Регион {code} закончен")
    print(f"Регион {code} закончен")


async def get_npa_api(client: httpx.AsyncClient) -> List[Tuple[str, str]]:
    """Асинхронно получает данные NPA."""
    names = []
    npa_ids = []
    try:
        resp = await client.get(get_type_all())
        resp.raise_for_status()
        data = resp.json()
        for npa in data:
            names.append(npa["name"])
            npa_ids.append(npa["id"])
    except httpx.RequestError as e:
        logger.error(f"Ошибка запроса NPA: {e}")
        return []
    except Exception as e:
        logger.error(f"Неизвестная ошибка при запросе NPA: {e}")
        return []
    return list(zip(names, npa_ids))


async def get_subject_api(client: httpx.AsyncClient) -> List[Tuple[str, str]]:
    """Асинхронно получает данные субъектов."""
    try:
        resp = await client.get(get_subjects())
        resp.raise_for_status()
        data = resp.json()
        names = [subject["name"] for subject in data]
        codes = [subject["code"] for subject in data]
    except httpx.RequestError as e:
        logger.error(f"Ошибка запроса субъектов: {e}")
        return []
    except Exception as e:
        logger.error(f"Неизвестная ошибка при запросе субъектов: {e}")
        return []

    other_codes = [
        "president",
        "council_1",
        "council_2",
        "government",
        "federal_authorities",
        "court",
        "international",
        "un_securitycouncil",
    ]
    other_names = [
        "Президент РФ",
        "Совет Федерации ФС РФ",
        "Государственная Дума ФС РФ",
        "Правительство РФ",
        "ФОИВ и ФГО РФ",
        "Конституционный Суд РФ",
        "Международные договоры РФ",
        "Совет Безопасности ООН",
    ]
    names.extend(other_names)
    codes.extend(other_codes)
    return list(zip(names, codes))


async def parse():
    """Основная функция парсинга."""
    logger.info("Начало парсинга")
    timeout = httpx.Timeout(30.0, connect=30.0)
    async with httpx.AsyncClient(proxy=PROXY, timeout=timeout) as client:
        name_code = await get_subject_api(client)
        name_npa_id = await get_npa_api(client)

        if not name_code or not name_npa_id:
            logger.error("Не удалось загрузить начальные данные, завершение парсинга")
            return

        await insert_act(name_npa_id)
        regions_inserted = await insert_region(name_code)
        if not regions_inserted:
            logger.warning(
                "Регионы не вставлены, дальнейшая обработка может быть некорректной"
            )
        await update_region([])  # Уточните subjects_data, если нужно

        for name, code in name_code:
            await get_document_api(code, client)


if __name__ == "__main__":
    asyncio.run(parse())
