import json
import parser.utils.utils as utils
from parser.database import raw
from parser.data.regions import get_regions_data


logger = utils.get_logger("database.query.update")


# class QueryUpdateInterface:

#     def table_regions():
#         return NotImplementedError


class QueryUpdate:

    connection = None

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
    def table_regions(self, cursor):
        values = [(region["id_dist"], region["name"]) for region in get_regions_data()]
        logger.debug(json.dumps(values, indent=4, ensure_ascii=False))

        args = ",".join(
            cursor.mogrify("(%s, %s, %s)", region).decode("utf-8") for region in values
        )
        return raw.UPDATE_TABLE_REGIONS + args
