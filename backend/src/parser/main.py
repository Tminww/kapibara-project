import asyncio
import json
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert

from config import settings
from database.setup import get_async_session
from utils.logger import parser_logger as logger
from models import ActEntity

INSERT_ACT = """INSERT INTO ACT (name, npa_id) VALUES """

INSERT_REGION = """INSERT INTO REGION (name, code) VALUES """

UPDATE_REGION_TABLE = """UPDATE region SET id_dist = %s WHERE name = %s"""

INSERT_DOCUMENT = """INSERT INTO DOCUMENT (complex_name, id_act, eo_number, view_date, pages_count, id_reg) VALUES """


async def insert_act(name_npaId):
    async with get_async_session() as session:
        try:
            # Подготовка данных для вставки
            values = [{"name": name, "npa_id": npa_id} for name, npa_id in name_npaId]

            # Создаем INSERT-запрос с ON CONFLICT
            stmt = (
                insert(ActEntity)
                .values(values)
                .on_conflict_do_nothing(
                    index_elements=[
                        "name",
                        "npa_id",
                    ]  # Указываем поля уникального индекса
                )
            )

            # Выполняем запрос
            await session.execute(stmt)
            await session.commit()
            logger.info(f"Successfully inserted {len(values)} records")

        except IntegrityError as e:
            await session.rollback()
            logger.exception("Unique constraint violation during bulk insert")
        except Exception as e:
            await session.rollback()
            logger.exception("Unexpected error during bulk insert")


def insert_region(name_code):
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            try:
                values = name_code
                args = ",".join(
                    cursor.mogrify("(%s, %s)", i).decode("utf-8") for i in values
                )
                cursor.execute(INSERT_REGION + args + " ON CONFLICT DO NOTHING;")

            except errors.lookup(UNIQUE_VIOLATION) as e:
                logger.exception(UNIQUE_VIOLATION)


def get_id_reg(code):
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT id from region WHERE code = '{code}';""")
            id_reg = cursor.fetchone()[0]
            return id_reg


def get_id_act(npa_id):
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT id FROM ACT WHERE npa_id = '{npa_id}';""")
            id_act = cursor.fetchone()[0]
            return id_act


def update_region():
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            try:
                values = get_subjects_data()
                for row in values:
                    cursor.execute(
                        UPDATE_REGION_TABLE, (row.get("id_dist", None), row["name"])
                    )
            except errors.lookup(UNIQUE_VIOLATION) as e:
                logger.exception(UNIQUE_VIOLATION)


def insert_document(
    complex_names, eo_numbers, pages_counts, view_dates, id_regs, id_acts
):
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            values = list(
                zip(
                    complex_names,
                    id_acts,
                    eo_numbers,
                    view_dates,
                    pages_counts,
                    id_regs,
                )
            )
            args = ",".join(
                cursor.mogrify("(%s, %s, %s, %s, %s, %s)", i).decode("utf-8")
                for i in values
            )
            try:
                cursor.execute(INSERT_DOCUMENT + args + " ON CONFLICT DO NOTHING;")
            except errors.lookup(UNIQUE_VIOLATION) as e:
                logger.exception(UNIQUE_VIOLATION)


def get_total_documents(code):
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""SELECT id from region WHERE code = '{code}';""")
                id_reg = cursor.fetchone()[0]

                cursor.execute(
                    f"""SELECT COUNT(*) FROM DOCUMENT WHERE 
                               id_reg = {id_reg};"""
                )
                count = cursor.fetchone()[0]
                print(count)
                return count
            except Exception as e:
                logger.exception(Exception)


def get_total_documents_type(code, npa_id):
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""SELECT id FROM ACT WHERE npa_id = '{npa_id}';""")
                id_act = cursor.fetchone()[0]

                cursor.execute(f"""SELECT id from region WHERE code = '{code}';""")
                id_reg = cursor.fetchone()[0]

                cursor.execute(
                    f"""SELECT COUNT(*) FROM DOCUMENT WHERE 
                               id_reg = {id_reg} and id_act = {id_act};"""
                )
                count = cursor.fetchone()[0]
                return count
            except Exception as e:
                logger.exception(Exception)


def regions_data():
    with open(f"{settings.BASE_DIR}/parser/mock/regions.json", "r") as file:
        data = json.load(file)
        return data


def districts_data():
    with open(f"{settings.BASE_DIR}/parser/mock/districts.json", "r") as file:
        data = json.load(file)
        return data


def get_documents_on_page(code):
    return f"{settings.EXTERNAL_URL}/api/Documents?block={code}&PageSize=200&Index=1"


def get_documents_on_page_type(npa_id, code, index):
    return f"{settings.EXTERNAL_URL}/api/Documents?DocumentTypes={npa_id}&block={code}&PageSize=200&Index={index}"


def get_subjects():
    return f"{settings.EXTERNAL_URL}/api/PublicBlocks/?parent=subjects"


def get_type_all():
    return f"{settings.EXTERNAL_URL}/api/DocumentTypes"


def get_type_in_subject(code):
    return f"{settings.EXTERNAL_URL}/api/DocumentTypes?block={code}"


async def parse():
    logger.info("Начало парсинга")
    print(districts_data())


if __name__ == "__main__":
    asyncio.run(parse())
