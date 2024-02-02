from database.setup import get_sync_connection
from data.districts import get_districts_data
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

from log.createLogger import get_logger


logging = get_logger("database.initial")

CREATE_REGION_TABLE = """
        CREATE TABLE IF NOT EXISTS region (
        id SERIAL NOT NULL, 
        id_dist INTEGER, 
        name VARCHAR(128) NOT NULL, 
        code VARCHAR(16) NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (name, code),
        FOREIGN KEY(id_dist) REFERENCES district (id)
        )
        """

CREATE_ACT_TABLE = """
        CREATE TABLE IF NOT EXISTS act (
        id SERIAL NOT NULL, 
        name VARCHAR(128) NOT NULL, 
        npa_id VARCHAR(128) NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (name, npa_id)
        )
        """

CREATE_DOCUMENT_TABLE = """
        CREATE TABLE IF NOT EXISTS document (
        id BIGSERIAL NOT NULL, 
        complex_name TEXT NOT NULL, 
        id_act INTEGER NOT NULL, 
        eo_number VARCHAR(16) NOT NULL, 
        view_date DATE NOT NULL, 
        pages_count INTEGER NOT NULL, 
        id_reg INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (id_reg, complex_name, eo_number), 
        FOREIGN KEY(id_act) REFERENCES act (id), 
        FOREIGN KEY(id_reg) REFERENCES region (id)
        )
        """

CREATE_DISTRICT_TABLE = """
        CREATE TABLE IF NOT EXISTS district (
        id INT PRIMARY KEY,
        name VARCHAR(50)
        )
        """

INSERT_DISTRICTS = """INSERT INTO DISTRICT (id, name) VALUES """

CREATE_ALL_INDEX = """CREATE INDEX IF NOT EXISTS document_id_idx ON document (id);
                    CREATE INDEX IF NOT EXISTS document_id_reg_idx ON document (id_reg);
                    CREATE INDEX IF NOT EXISTS document_view_date_idx ON document (view_date);
                    """

def create_tables():
    create_district_table()
    insert_district_table()
    create_region_table()
    create_act_table()
    create_document_table()
    create_all_index()

    logging.info("Таблицы созданы или уже существуют")

def create_all_index():
        with get_sync_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_ALL_INDEX)

def create_district_table():
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_DISTRICT_TABLE)


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
                logging.exception(UNIQUE_VIOLATION)


def create_region_table():
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_REGION_TABLE)


def create_act_table():
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ACT_TABLE)


def create_document_table():
    with get_sync_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_DOCUMENT_TABLE)
