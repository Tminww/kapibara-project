from parser.database.database import db
from parser.data.districts import get_districts_data


def test_create_table_districts():
    status = db.initiate.create.table_districts()
    assert status == True


def test_create_table_regions():
    status = db.initiate.create.table_regions()
    assert status == True


def test_create_table_receiving_authorities():
    status = db.initiate.create.table_receiving_authorities()
    assert status == True


def test_create_table_blocks():
    status = db.initiate.create.table_blocks()
    assert status == True


def test_create_table_deadlines():
    status = db.initiate.create.table_deadlines()
    assert status == True


def test_create_table_document_types():
    status = db.initiate.create.table_document_types()
    assert status == True


def test_create_table_document_types__blocks():
    status = db.initiate.create.table_document_types__blocks()
    assert status == True


def test_create_table_documents():
    status = db.initiate.create.table_documents()
    assert status == True


def test_create_table_roles():
    status = db.initiate.create.table_roles()
    assert status == True


def test_create_table_users():
    status = db.initiate.create.table_users()
    assert status == True


def test_create_all_index():
    status = db.initiate.create.index_all()
    assert status == True


def test_insert_table_districts():
    status = db.initiate.insert.table_districts(json_data=get_districts_data())
    assert status == True
