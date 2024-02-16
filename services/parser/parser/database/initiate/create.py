from psycopg2.errorcodes import UNIQUE_VIOLATION

import parser.database.raw as raw
from psycopg2 import errors

import parser.utils.utils as utils


logger = utils.get_logger("database.initiate.create")


class InitiateCreateInterface:

    def table_districts():
        raise NotImplementedError

    def table_regions():
        raise NotImplementedError

    def table_receiving_authorities():
        raise NotImplementedError

    def table_blocks():
        raise NotImplementedError

    def table_deadlines():
        raise NotImplementedError

    def table_document_types():
        raise NotImplementedError

    def table_document_types__blocks():
        raise NotImplementedError

    def table_documents():
        raise NotImplementedError

    def table_roles():
        raise NotImplementedError

    def table_users():
        raise NotImplementedError

    def index_all():
        raise NotImplementedError


class InitiateCreate(InitiateCreateInterface):

    connection = None

    def __init__(self, get_connection) -> None:
        self.connection = get_connection

    def query_create(func):
        def wrapper(self, *args, **kwargs):
            status = False
            with self.connection() as connection:
                with connection.cursor() as cursor:
                    try:
                        stmt = func(self, *args, **kwargs)
                        cursor.execute(stmt)
                        status = True
                        logger.info(f"{func.__name__} успешно выполнена")
                    except Exception as ex:
                        logger.critical(f"{func.__name__} завершилась с ошибкой {ex}")
            return status

        return wrapper

    @query_create
    def table_districts(self):
        return raw.CREATE_TABLE_DISTRICTS

    @query_create
    def table_regions(self):
        return raw.CREATE_TABLE_REGIONS

    @query_create
    def table_receiving_authorities(self):
        return raw.CREATE_TABLE_RECEIVING_AUTHORITIES

    @query_create
    def table_blocks(self):
        return raw.CREATE_TABLE_BLOCKS

    @query_create
    def table_deadlines(self):
        return raw.CREATE_TABLE_DEADLINES

    @query_create
    def table_document_types(self):
        return raw.CREATE_TABLE_DOCUMENT_TYPES

    @query_create
    def table_document_types__blocks(self):
        return raw.CREATE_TABLE_DOCUMENT_TYPES__BLOCKS

    @query_create
    def table_documents(self):
        return raw.CREATE_TABLE_DOCUMENTS

    @query_create
    def table_roles(self):
        return raw.CREATE_TABLE_ROLES

    @query_create
    def table_users(self):
        return raw.CREATE_TABLE_USERS

    @query_create
    def index_all(self):
        return raw.CREATE_INDEX_ALL
