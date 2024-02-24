import json
import pprint
from psycopg2.errorcodes import UNIQUE_VIOLATION

import parser.database.raw as raw
from psycopg2 import errors

import parser.utils.utils as utils
from parser.data.districts import get_districts_data


logger = utils.get_logger("database.initiate.insert")


class InitiateInsertInterface:

    def table_districts():
        raise NotImplementedError

    def table_deadlines():
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
    def table_districts(self, cursor, json_data=get_districts_data()):

        values = [
            (district["id"], district["name"], district["short_name"])
            for district in json_data
        ]
        logger.debug(json.dumps(values, indent=4, ensure_ascii=False))
        args = ",".join(
            cursor.mogrify("(%s, %s, %s)", district).decode("utf-8")
            for district in values
        )
        return (
            raw.INSERT_INTO_TABLE_DISTRICTS
            + args
            + " ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, short_name = EXCLUDED.short_name;"
        )

    @query_insert
    def table_deadlines():
        pass
