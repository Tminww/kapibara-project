from parser.api.api import (
    get_blocks,
    get_documents_on_page,
    get_documents_on_page_type,
    get_subjects,
    get_type_all,
    get_type_in_subject,
)


def test_get_blocks():
    assert (
        get_blocks() == "http://publication.pravo.gov.ru/api/PublicBlocks/?Categories"
    )


def test_get_document_on_page():
    assert (
        get_documents_on_page("block")
        == f"http://publication.pravo.gov.ru/api/Documents?block=block&PageSize=200&Index=1"
    )
