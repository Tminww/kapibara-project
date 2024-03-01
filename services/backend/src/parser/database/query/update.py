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
