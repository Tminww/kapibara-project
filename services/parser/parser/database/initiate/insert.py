import json
import pprint
from typing import List
from psycopg2.errorcodes import UNIQUE_VIOLATION

import parser.database.raw as raw
from psycopg2 import errors

import parser.utils.utils as utils
from parser.data.districts import get_districts_data


logger = utils.get_logger("database.initiate.insert")

ID_DEADLINE = 0
HASH = "x7585xx8969"


# class InitiateInsertInterface:

#     def table_districts(json_data: List[dict]):
#         raise NotImplementedError

#     def table_deadlines(json_data: List[dict]):
#         raise NotImplementedError

#     def table_regions(blocks: List[dict]):
#         raise NotImplementedError

#     def table_document_types(types: List[dict]):
#         raise NotImplementedError

#     def table_receiving_authorities(types: List[dict]):
#         raise NotImplementedError


class InitiateInsert:
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
    def table_districts(self, cursor, json_data: List[dict]):

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
    def table_regions(self, cursor, blocks: List[dict]):
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
            cursor.mogrify("(%s, %s, %s, %s, %s)", i).decode("utf-8") for i in values
        )
        return raw.INSERT_INTO_TABLE_REGIONS + args + " ON CONFLICT DO NOTHING;"

    @query_insert
    def table_document_types(self, cursor, types: List[dict]):

        values = [(type["name"], type["external_id"], ID_DEADLINE) for type in types]
        args = ",".join(
            cursor.mogrify("(%s, %s, %s)", i).decode("utf-8") for i in values
        )
        return raw.INSERT_INTO_TABLE_TYPES + args + " ON CONFLICT DO NOTHING;"

    @query_insert
    def table_deadlines(self, cursor, deadlines: List[dict]):

        values = [(deadline["id"], deadline["day"]) for deadline in deadlines]
        args = ",".join(cursor.mogrify("(%s, %s)", i).decode("utf-8") for i in values)
        return (
            raw.INSERT_INTO_TABLE_DEADLINES
            + args
            + " ON CONFLICT (day) DO UPDATE SET day = EXCLUDED.day;"
        )

    @query_insert
    def table_receiving_authorities(self, cursor, types: List[dict]):

        values = [(type["name"], type["short_name"], type["code"]) for type in types]
        args = ",".join(
            cursor.mogrify("(%s, %s, %s)", i).decode("utf-8") for i in values
        )
        return (
            raw.INSERT_INTO_TABLE_RECEIVING_AUTHORITIES
            + args
            + " ON CONFLICT (name, short_name, code) DO UPDATE SET name = EXCLUDED.name, short_name = EXCLUDED.short_name, code = EXCLUDED.code;"
        )
