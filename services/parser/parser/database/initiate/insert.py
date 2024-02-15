from psycopg2.errorcodes import UNIQUE_VIOLATION

import parser.database.raw as raw
from psycopg2 import errors

import parser.utils.utils as utils
from parser.data.districts import get_districts_data


logger = utils.get_logger("database.initiate.insert")


class InitiateInsertInterface:

    def insert_table_districts():
        raise NotImplementedError


class InitiateInsert(InitiateInsertInterface):
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
    def insert_table_districts(self, cursor):

        values = get_districts_data()
        args = ",".join(
            cursor.mogrify(
                "(%s, %s, %s)", (row["id"], row["name"], row["short_name"])
            ).decode("utf-8")
            for row in values
        )
        return (
            raw.INSERT_DISTRICTS
            + args
            + " ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;"
        )
