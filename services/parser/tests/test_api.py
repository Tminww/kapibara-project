from parser.api.api import api


def test_get_blocks():
    response = api.publication.blocks()
    assert response["response"].status_code == 200
    assert response["response"].json() != None


def test_get_document_on_page():
    response = api.publication.documents_on_page("region01")
    assert response["response"].status_code == 200
    assert response["response"].json() != None


def test_documents_on_page_type():
    response = api.publication.documents_on_page_type(
        block="region01", npa_id="63c6ff4f-ed74-45b3-86e2-8a76b75d674d", index=1
    )
    print(response)
    assert response["response"].status_code == 200
    assert response["response"].json() != None


def test_type_in_subject():
    response = api.publication.type_in_subject(block="region01")
    assert response["response"].status_code == 200
    assert response["response"].json() != None


def test_type_all():
    response = api.publication.type_all()
    assert response["response"].status_code == 200
    assert response["response"].json() != None
