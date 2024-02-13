from parser.database.setup import get_sync_connection
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors
from parser.data.subjects import get_subjects_data

import parser.utils.utils as utils


logger = utils.get_logger("database.query")


def insert_types(types):
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            try:
                values = [(type["name"], type["external_id"]) for type in types]
                args = ",".join(
                    cursor.mogrify("(%s, %s)", i).decode("utf-8") for i in values
                )
                cursor.execute(INSERT_TYPES + args + " ON CONFLICT DO NOTHING;")
                logger.info(f"Вставленно {len(values)} номенклатур")
            except errors.lookup(UNIQUE_VIOLATION) as e:
                logger.exception(UNIQUE_VIOLATION)


def insert_regions(blocks):
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            try:
                values = [
                    (
                        block["name"],
                        block["short_name"],
                        block["external_id"],
                        block["code"],
                        block["parent_id"],
                    )
                    for block in blocks
                ]
                args = ",".join(
                    cursor.mogrify("(%s, %s, %s, %s, %s)", i).decode("utf-8")
                    for i in values
                )
                cursor.execute(INSERT_SUBJECTS + args + " ON CONFLICT DO NOTHING;")
                logger.info(f"Вставленно {len(values)} регионов")

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


def update_subjects():
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            try:
                values = get_subjects_data()
                for row in values:
                    cursor.execute(UPDATE_REGION_TABLE, (row["id_dist"], row["name"]))

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
