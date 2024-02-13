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

CREATE_TABLE_DOCUMENT_TYPES = """
        CREATE TABLE IF NOT EXISTS document_types  (
            id SERIAL PRIMARY KEY, 
            name VARCHAR(128), 
            external_id VARCHAR(64),
            id_dl INT,
            
            FOREIGN KEY(id_dl) REFERENCES Deadlines (id), 
            UNIQUE (name, external_id)
        )
        """

CREATE_TABLE_DOCUMENT_TYPES__BLOCKS = """
        CREATE TABLE IF NOT EXISTS document_types__blocks  (
            id SERIAL PRIMARY KEY, 
            id_doc_type INT, 
            id_block INT,
            
            FOREIGN KEY(id_doc_type) REFERENCES document_types (id),
            FOREIGN KEY(id_block) REFERENCES blocks (id),
            UNIQUE (id_doc_type, id_block)
        )
        """

CREATE_TABLE_DOCUMENTS = """
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


CREATE_ALL_INDEX = """CREATE INDEX IF NOT EXISTS document_id_idx ON documents (id);
                    CREATE INDEX IF NOT EXISTS document_id_reg_idx ON documents (id_doc_type_block);
                    CREATE INDEX IF NOT EXISTS document_view_date_idx ON documents (view_date);
                    """

INSERT_DISTRICTS = """INSERT INTO DISTRICT (id, name) VALUES """


INSERT_TYPES = """INSERT INTO ACT (name, external_id) VALUES """

INSERT_SUBJECTS = (
    """INSERT INTO REGION (name, short_name, external_id, code, parent_id) VALUES """
)

UPDATE_REGION_TABLE = """UPDATE region SET id_dist = %s WHERE name = %s"""

INSERT_DOCUMENT = """INSERT INTO DOCUMENT (complex_name, id_act, eo_number, view_date, pages_count, id_reg) VALUES """
