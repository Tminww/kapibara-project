import parser.utils.utils as utils
from parser.database import raw

logger = utils.get_logger("database.query.select")


# class QuerySelectInterface:

#     # def update_table_regions():
#     #     return NotImplementedError
#     pass


class QuerySelect:
    connection = None

    def __init__(self, get_connection) -> None:
        self.connection = get_connection


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
