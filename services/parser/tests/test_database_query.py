from parser.database.database import db


def test_insert_into_table_regions():
    blocks = [
        {
            "name": "first",
            "short_name": "shortName",
            "external_id": "id",
            "code": "code",
            "parent_id": "parentId",
        },
        {
            "name": "first",
            "short_name": "shortName",
            "external_id": "id",
            "code": "code",
            "parent_id": "parentId",
        },
    ]
    status = db.query.insert.into_table_regions(blocks)
    assert status == True


def test_create_table_regions():
    documents = [
        {
            "name": "first",
            "eo_number": "1",
            "view_date": "2000-02-02",
            "pages_count": "2",
        },
        {
            "name": "second",
            "eo_number": "2",
            "view_date": "2000-02-02",
            "pages_count": "2",
        },
    ]
    status = db.query.insert.into_table_documents(documents)
    assert status == True
