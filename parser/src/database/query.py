from database.setup import get_sync_connection
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors
from data.subjects import get_subjects_data

from log.createLogger import get_logger


logging = get_logger()

INSERT_ACT = """INSERT INTO ACT (name, npa_id) VALUES """

INSERT_REGION = """INSERT INTO REGION (name, code) VALUES """

UPDATE_REGION_TABLE = """UPDATE region SET id_dist = %s WHERE name = %s"""

INSERT_DOCUMENT = """INSERT INTO DOCUMENT (complex_name, id_act, eo_number, view_date, pages_count, id_reg) VALUES """


def insert_act(name_npaId):
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            try:
                values = name_npaId
                args = ",".join(
                    cursor.mogrify("(%s, %s)", i).decode("utf-8") for i in values
                )
                cursor.execute(INSERT_ACT + args + " ON CONFLICT DO NOTHING;")
            except errors.lookup(UNIQUE_VIOLATION) as e:
                logging.exception(UNIQUE_VIOLATION)


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
                logging.exception(UNIQUE_VIOLATION)


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
                    cursor.execute(UPDATE_REGION_TABLE, (row.get("id_dist", None), row["name"]))
            except errors.lookup(UNIQUE_VIOLATION) as e:
                logging.exception(UNIQUE_VIOLATION)


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
                logging.exception(UNIQUE_VIOLATION)


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
                logging.exception(Exception)


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
                logging.exception(Exception)
