import json
import pprint
from typing import List
from psycopg2.errorcodes import UNIQUE_VIOLATION

import parser.database.raw as raw
from psycopg2 import errors

from utils import utils
from parser.assets.districts.data import get_districts_data


logger = utils.get_logger("database.initiate.insert")


class InitiateUpdate:

    def __init__(self, get_connection) -> None:
        self.connection = get_connection

    def query_update(func):
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

    @query_update
    def table_regions(self, cursor, mock_data: List[dict]):
        values = [(region["id_dist"], region["name"]) for region in mock_data]
        logger.debug(json.dumps(values, indent=4, ensure_ascii=False))

        args = ",".join(
            cursor.mogrify("(%s, %s, %s)", region).decode("utf-8") for region in values
        )
        return raw.UPDATE_TABLE_REGIONS + args
