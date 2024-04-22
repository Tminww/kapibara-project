from utils import utils
from parser.database import raw

logger = utils.get_logger("database.query.select")


class QuerySelect:

    def __init__(self, get_connection) -> None:
        self.connection = get_connection

    def query_insert(func):
        def wrapper(self, *args, **kwargs):
            status = False
            with self.connection() as connection:
                with connection.cursor() as cursor:
                    try:
                        stmt = func(self, cursor, *args, **kwargs)
                        cursor.execute(stmt)
                        status = True
                        logger.info(f"{func.__name__} успешно выполнена")
                    except Exception as ex:
                        logger.critical(f"{func.__name__} завершилась с ошибкой {ex}")
            return status

        return wrapper

    def get_row(self, table: str, column: list, where: dict):

        columns = ",".join(column)

        where_params = [f"{pair} = '{pair.get(pair)}'" for pair in where]

        # cursor.execute(f"SELECT {columns} from {table} WHERE {where_params};")
        # answer = cursor
        # return answer
        logger.debug(f"SELECT {columns} from {table} WHERE {where_params};")
        print(f"SELECT {columns} from {table} WHERE {where_params};")
        return f"SELECT {columns} from {table} WHERE {where_params};"

    # def get_id_act(npa_id):
    #     with get_sync_connection() as connection:
    #         with connection.cursor() as cursor:
    #             cursor.execute(f"""SELECT id FROM ACT WHERE npa_id = '{npa_id}';""")
    #             id_act = cursor.fetchone()[0]
    #             return id_act

    # def get_total_documents(code):
    #     with get_sync_connection() as connection:
    #         with connection.cursor() as cursor:
    #             try:
    #                 cursor.execute(f"""SELECT id from region WHERE code = '{code}';""")
    #                 id_reg = cursor.fetchone()[0]

    #                 cursor.execute(
    #                     f"""SELECT COUNT(*) FROM DOCUMENT WHERE
    #                             id_reg = {id_reg};"""
    #                 )
    #                 count = cursor.fetchone()[0]
    #                 return count
    #             except Exception as e:
    #                 logger.exception(Exception)

    # def get_total_documents_type(code, npa_id):
    #     with get_sync_connection() as connection:
    #         with connection.cursor() as cursor:
    #             try:
    #                 cursor.execute(f"""SELECT id FROM ACT WHERE npa_id = '{npa_id}';""")
    #                 id_act = cursor.fetchone()[0]

    #                 cursor.execute(f"""SELECT id from region WHERE code = '{code}';""")
    #                 id_reg = cursor.fetchone()[0]

    #                 cursor.execute(
    #                     f"""SELECT COUNT(*) FROM DOCUMENT WHERE
    #                             id_reg = {id_reg} and id_act = {id_act};"""
    #                 )
    #                 count = cursor.fetchone()[0]
    #                 return count
    #             except Exception as e:
    #                 logger.exception(Exception)
