import asyncio
from datetime import datetime
import json
from typing import List, Tuple
import httpx  # Заменяем aiohttp на httpx
from sqlalchemy import func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from config import settings
from database.setup import get_async_session
from utils.logger import parser_logger as logger
from models import ActEntity, RegionEntity, DocumentEntity

# Определяем декоратор
async_session_maker = (
    get_async_session  # Предполагается, что это возвращает async_sessionmaker
)


@connection
async def insert_act(name_npaId: List[Tuple[str, str]], session: AsyncSession):
    """Вставляет записи в таблицу acts асинхронно."""
    values = [{"name": name, "npa_id": npa_id} for name, npa_id in name_npaId]
    stmt = (
        insert(ActEntity)
        .values(values)
        .on_conflict_do_nothing(index_elements=["name", "npa_id"])
    )
    await session.execute(stmt)
    await session.commit()
    logger.info(f"Successfully inserted {len(values)} acts")


@connection
async def insert_region(name_code: List[Tuple[str, str]], session: AsyncSession):
    """Вставляет записи в таблицу regions асинхронно."""
    values = [{"name": name, "code": code} for name, code in name_code]
    stmt = (
        insert(RegionEntity)
        .values(values)
        .on_conflict_do_nothing(index_elements=["name", "code"])
    )
    await session.execute(stmt)
    await session.commit()
    logger.info(f"Successfully inserted {len(values)} regions")


@connection
async def get_id_reg(code: str, session: AsyncSession) -> int:
    """Получает ID региона по коду."""
    stmt = select(RegionEntity.id).where(RegionEntity.code == code)
    result = await session.execute(stmt)
    id_reg = result.scalar_one_or_none()
    if id_reg is None:
        raise ValueError(f"Region with code {code} not found")
    return id_reg


@connection
async def get_id_act(npa_id: str, session: AsyncSession) -> int:
    """Получает ID акта по npa_id."""
    stmt = select(ActEntity.id).where(ActEntity.npa_id == npa_id)
    result = await session.execute(stmt)
    id_act = result.scalar_one_or_none()
    if id_act is None:
        raise ValueError(f"Act with npa_id {npa_id} not found")
    return id_act


@connection
async def update_region(subjects_data: List[dict], session: AsyncSession):
    """Обновляет таблицу regions с id_dist."""
    for row in subjects_data:
        stmt = (
            update(RegionEntity)
            .where(RegionEntity.name == row["name"])
            .values(id_dist=row.get("id_dist"))
        )
        await session.execute(stmt)
    await session.commit()
    logger.info(f"Updated {len(subjects_data)} regions")


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


@connection
async def get_total_documents(code: str, session: AsyncSession) -> int:
    """Подсчитывает общее количество документов для региона."""
    id_reg = await get_id_reg(code, session=session)
    stmt = (
        select(func.count())
        .select_from(DocumentEntity)
        .where(DocumentEntity.id_reg == id_reg)
    )
    result = await session.execute(stmt)
    count = result.scalar()
    logger.info(f"Total documents for region {code}: {count}")
    return count


@connection
async def get_total_documents_type(
    code: str, npa_id: str, session: AsyncSession
) -> int:
    """Подсчитывает количество документов определённого типа для региона."""
    id_reg = await get_id_reg(code, session=session)
    id_act = await get_id_act(npa_id, session=session)
    stmt = (
        select(func.count())
        .select_from(DocumentEntity)
        .where(DocumentEntity.id_reg == id_reg, DocumentEntity.id_act == id_act)
    )
    result = await session.execute(stmt)
    count = result.scalar()
    logger.info(f"Total documents for region {code} and npa_id {npa_id}: {count}")
    return count


def regions_data() -> List[dict]:
    """Загружает данные регионов из JSON."""
    with open(f"{settings.BASE_DIR}/parser/mock/regions.json", "r") as file:
        return json.load(file)


def districts_data() -> List[dict]:
    """Загружает данные районов из JSON."""
    with open(f"{settings.BASE_DIR}/parser/mock/districts.json", "r") as file:
        return json.load(file)


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

    # Запрос общего количества документов
    resp = await client.get(get_documents_on_page(code))
    if resp.status_code != 200:
        logger.error(f"Ошибка при запросе: статус {resp.status_code}")
        return
    total_documents_data = resp.json()

    # Проверка, нужно ли обновлять данные
    if await get_total_documents(code) == total_documents_data.get("itemsTotalCount"):
        logger.info(f"Регион {code} уже заполнен")
        print(f"Регион {code} уже заполнен")
        return

    # Запрос типов документов
    resp = await client.get(get_type_in_subject(code))
    if resp.status_code != 200:
        logger.error(f"Ошибка при запросе типов документов: статус {resp.status_code}")
        return
    type_data = resp.json()

    # Обработка каждого типа документа
    for npa in type_data:
        current_page = 1
        while True:
            await asyncio.sleep(0.5)  # Асинхронная задержка
            url = get_documents_on_page_type(npa["id"], code, current_page)
            resp = await client.get(url)
            if resp.status_code != 200:
                logger.error(
                    f"Ошибка при запросе документов: статус {resp.status_code}"
                )
                break
            documents_data = resp.json()

            # Проверка, нужно ли обновлять данные
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

                for item in documents_data.get("items", []):
                    complex_names.append(item.get("complexName"))
                    eo_numbers.append(item.get("eoNumber"))
                    pages_counts.append(item.get("pagesCount"))
                    view_dates.append(
                        datetime.strptime(item.get("viewDate"), "%d.%m.%Y").strftime(
                            "%Y-%m-%d"
                        )
                    )
                    id_regs.append(id_reg)
                    id_acts.append(id_act)

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
    resp = await client.get(get_type_all())
    data = resp.json()
    for npa in data:
        names.append(npa["name"])
        npa_ids.append(npa["id"])
    return list(zip(names, npa_ids))


async def get_subject_api(client: httpx.AsyncClient) -> List[Tuple[str, str]]:
    """Асинхронно получает данные субъектов."""
    resp = await client.get(get_subjects())
    data = resp.json()
    names = [subject["name"] for subject in data]
    codes = [subject["code"] for subject in data]

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
    async with httpx.AsyncClient() as client:
        name_code = await get_subject_api(client)
        name_npa_id = await get_npa_api(client)

        await insert_act(name_npa_id)
        await insert_region(name_code)
        await update_region([])  # Уточните subjects_data, если нужно

        for name, code in name_code:
            await get_document_api(code, client)


if __name__ == "__main__":
    asyncio.run(parse())
