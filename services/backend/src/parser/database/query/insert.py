import random
from typing import List


import parser.utils.utils as utils
from parser.database import raw


logger = utils.get_logger("database.query.insert")

ID_DEADLINE = 0
HASH = "x7585xx8969"


# class QueryInsertInterface:

#     def table_documents(documents: List[dict]):
#         raise NotImplementedError


class QueryInsert:
    connection = None

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

    @query_insert
    def table_documents(self, cursor, documents: List[dict]):
        values = [
            (
                document["name"],
                document["eo_number"],
                document["view_date"],
                # document["hash"],
                random.getrandbits(128),
                document["pages_count"],
                # document["id_doc_type_block"],
            )
            for document in documents
        ]
        args = ",".join(
            cursor.mogrify("(%s, %s, %s, %s, %s)", document).decode("utf-8")
            for document in values
        )
        return raw.INSERT_INTO_TABLE_DOCUMENTS + args + " ON CONFLICT DO NOTHING;"
