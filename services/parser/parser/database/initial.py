from parser.database.setup import get_sync_connection
from parser.data.districts import get_districts_data
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

import parser.utils.utils as utils


logger = utils.get_logger("database.initial")

CREATE_TABLE_DISTRICTS = """
        CREATE TABLE IF NOT EXISTS districts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            short_name VARCHAR(10),

            UNIQUE (name, short_name)
        )
        """

CREATE_TABLE_REGIONS = """
        CREATE TABLE IF NOT EXISTS regions (
            id SERIAL PRIMARY KEY, 
            name VARCHAR(128), 
            short_name VARCHAR(10),
            external_id VARCHAR(64),
            code VARCHAR(10),
            parent_id VARCHAR(64),
            id_dist INTEGER, 

            UNIQUE (name, short_name, external_id, code),
            FOREIGN KEY(id_dist) REFERENCES districts (id)
        )
        """
CREATE_TABLE_RECEIVING_AUTHORITIES = """
        CREATE TABLE IF NOT EXISTS receiving_authorities (
            id SERIAL PRIMARY KEY, 
            name VARCHAR(128), 
            short_name VARCHAR(50),
            code VARCHAR(50),

            UNIQUE (name, short_name, code)
        )
        """

CREATE_TABLE_BLOCKS = """
        CREATE TABLE IF NOT EXISTS blocks  (
            id SERIAL PRIMARY KEY, 
            name VARCHAR(128), 
            short_name VARCHAR(50),
            id_organ INT,
            id_reg INT NULL,

            FOREIGN KEY(id_organ) REFERENCES receiving_authorities (id), 
            FOREIGN KEY(id_reg) REFERENCES regions (id), 
            UNIQUE (name, short_name, id_organ, id_reg)
        )
        """

CREATE_TABLE_DEADLINES = """
        CREATE TABLE IF NOT EXISTS deadlines  (
            id SERIAL PRIMARY KEY, 
            day INT, 

            UNIQUE (day)
        )
        """

CREATE_DOCUMENT_TYPES_TABLE = """
        CREATE TABLE IF NOT EXISTS document_types  (
            id SERIAL PRIMARY KEY, 
            name VARCHAR(128), 
            external_id VARCHAR(64),
            id_dl INT,
            
            FOREIGN KEY(id_dl) REFERENCES Deadlines (id), 
            UNIQUE (name, short_name, external_id)
        )
        """

CREATE_DOCUMENT_TYPES__BLOCKS_TABLE = """
        CREATE TABLE IF NOT EXISTS document_types__blocks  (
            id SERIAL PRIMARY KEY, 
            id_doc_type INT, 
            id_block INT,
            
            FOREIGN KEY(id_doc_type) REFERENCES document_types (id),
            FOREIGN KEY(id_block) REFERENCES blocks (id),
            UNIQUE (id_doc_type, id_block)
        )
        """

CREATE_TEBLE_DOCUMENTS = """
        CREATE TABLE IF NOT EXISTS documents (
        id BIGSERIAL PRIMARY KEY, 
        name TEXT NOT NULL,
        eo_number VARCHAR(16), 
        view_date DATE, 
        hash VARCHAR(128),
        pages_count INT, 
        id_doc_type_block INT, 
        
        UNIQUE (name, eo_number, hash, id_doc_type_block), 
        FOREIGN KEY(id_doc_type_block) REFERENCES document_types__blocks (id)
    )
    """

CREATE_TABLE_ROLES = """
        CREATE TABLE IF NOT EXISTS roles (
            id serial PRIMARY KEY, 
            name VARCHAR(32),
            
            UNIQUE (name)
        )
        """

CREATE_TABLE_USERS = """
        CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY, 
            username VARCHAR(16),
            id_role INT,
            hash_password VARCHAR(16), 
            date_registered TIMESTAMP, 
            last_login TIMESTAMP,
            is_active bool, 
            
            UNIQUE (username), 
            FOREIGN KEY(id_role) REFERENCES roles (id)
        )
        """


INSERT_DISTRICTS = """INSERT INTO DISTRICT (id, name) VALUES """

CREATE_ALL_INDEX = """CREATE INDEX IF NOT EXISTS document_id_idx ON document (id);
                    CREATE INDEX IF NOT EXISTS document_id_reg_idx ON document (id_doc_type_block);
                    CREATE INDEX IF NOT EXISTS document_view_date_idx ON document (view_date);
                    """


def create_tables():
    create_districts_table()
    insert_districts_table()
    create_regions_table()
    create_act_table()
    create_document_table()
    create_all_index()

    logger.info("Таблицы созданы или уже существуют")


def create_all_index():
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(CREATE_ALL_INDEX)
                logger.info("Индексы созданы или уже существуют")
            except Exception as e:
                logger.critical(f"Индексы не созданы! {e}")


def create_table_districts():
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(CREATE_TABLE_DISTRICTS)
                logger.info("Округа созданы или уже существуют")
            except Exception as e:
                logger.critical(f"Округа не созданы! {e}")


def create_table_districts():
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(CREATE_TABLE_DISTRICTS)
                logger.info("Округа созданы или уже существуют")
            except Exception as e:
                logger.critical(f"Округа не созданы! {e}")


def insert_district_table():
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            try:
                values = get_districts_data()
                args = ",".join(
                    cursor.mogrify("(%s, %s)", (row["id"], row["name"])).decode("utf-8")
                    for row in values
                )
                cursor.execute(
                    INSERT_DISTRICTS
                    + args
                    + " ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;"
                )

            except errors.lookup(UNIQUE_VIOLATION) as e:
                logger.exception(UNIQUE_VIOLATION)


def create_region_table():
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(CREATE_REGION_TABLE)
                logger.info("Регионы созданы или уже существуют")
            except Exception as e:
                logger.critical(f"Регионы не созданы! {e}")


def create_act_table():
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(CREATE_ACT_TABLE)
                logger.info("Номенклатура созданы или уже существуют")
            except Exception as e:
                logger.critical(f"Номенклатура не созданы! {e}")


def create_document_table():
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(CREATE_DOCUMENT_TABLE)
                logger.info("Документы созданы или уже существуют")
            except Exception as e:
                logger.critical(f"Документы не созданы! {e}")
