from abc import ABC, abstractmethod
from parser.data.districts import get_districts_data
from psycopg2.errorcodes import UNIQUE_VIOLATION

import parser.database.raw as raw
from psycopg2 import errors

import parser.utils.utils as utils


logger = utils.get_logger("database.initiate")


class InitiateInterface(ABC):

    @abstractmethod
    def create_table_districts():
        raise NotImplementedError

    @abstractmethod
    def create_table_regions():
        raise NotImplementedError

    @abstractmethod
    def create_table_receiving_authorities():
        raise NotImplementedError

    @abstractmethod
    def create_table_blocks():
        raise NotImplementedError

    @abstractmethod
    def create_table_deadlines():
        raise NotImplementedError

    @abstractmethod
    def create_table_document_types():
        raise NotImplementedError

    @abstractmethod
    def create_table_document_types__blocks():
        raise NotImplementedError

    @abstractmethod
    def create_table_documents():
        raise NotImplementedError

    @abstractmethod
    def create_table_roles():
        raise NotImplementedError

    @abstractmethod
    def create_table_users():
        raise NotImplementedError

    @abstractmethod
    def create_all_index():
        raise NotImplementedError

    @abstractmethod
    def insert_into_table_districts():
        raise NotImplementedError


class Initiate(InitiateInterface):

    connection = None

    def __init__(self, get_connection) -> None:
        self.connection = get_connection

    def query(func):
        def wrapper(self, *args, **kwargs):
            status = False
            with self.connection() as connection:
                with connection.cursor() as cursor:
                    try:
                        cursor.execute(func(self, *args, **kwargs))
                        status = True
                        logger.info(f"{func.__name__} успешно выполнена")
                    except Exception as ex:
                        logger.critical(f"{func.__name__} завершилась с ошибкой {ex}")
            return status

        return wrapper

    @query
    def create_table_districts(self):
        return raw.CREATE_TABLE_DISTRICTS

    @query
    def create_table_regions(self):
        return raw.CREATE_TABLE_REGIONS

    @query
    def create_table_receiving_authorities(self):
        return raw.CREATE_TABLE_RECEIVING_AUTHORITIES

    @query
    def create_table_blocks(self):
        return raw.CREATE_TABLE_BLOCKS

    @query
    def create_table_deadlines(self):
        return raw.CREATE_TABLE_DEADLINES

    @query
    def create_table_document_types(self):
        return raw.CREATE_TABLE_DOCUMENT_TYPES

    @query
    def create_table_document_types__blocks(self):
        return raw.CREATE_TABLE_DOCUMENT_TYPES__BLOCKS

    @query
    def create_table_documents(self):
        return raw.CREATE_TABLE_DOCUMENTS

    @query
    def create_table_roles(self):
        return raw.CREATE_TABLE_ROLES

    @query
    def create_table_users(self):
        return raw.CREATE_TABLE_USERS

    @query
    def create_all_index(self):
        return raw.CREATE_ALL_INDEX

    @query
    def insert_into_table_districts(self):
        pass


# def insert_district_table():
#     with get_sync_connection() as connection:
#         with connection.cursor() as cursor:
#             try:
#                 values = get_districts_data()
#                 args = ",".join(
#                     cursor.mogrify("(%s, %s)", (row["id"], row["name"])).decode("utf-8")
#                     for row in values
#                 )
#                 cursor.execute(
#                     INSERT_DISTRICTS
#                     + args
#                     + " ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;"
#                 )

#             except errors.lookup(UNIQUE_VIOLATION) as e:
#                 logger.exception(UNIQUE_VIOLATION)
