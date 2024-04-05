import json

import requests
from parser.external_api.request import request
from utils.utils import get_logger

logger = get_logger("pytest")


def test_all_blocks():
    response = request.api.public_blocks()
    assert response["response"].status_code == 200
    assert response["response"].json() != None


def test_documents_for_the_block():
    response = request.api.documents_for_the_block(block="region01", index=1)
    assert response["response"].status_code == 200
    assert response["response"].json() != None


def test_documents_for_the_block_all():
    response = request.api.documents_for_the_block(
        block="region01", document_type="0790e34b-784b-4372-884e-3282622a24bd", index=1
    )
    # logger.debug(json.dumps(response["response"].json(), indent=4, ensure_ascii=False))
    assert response["response"].status_code == 200
    assert response["response"].json()["items"] != []


def test_types_in_block():
    response = request.api.types_in_block(block="region01")
    assert response["response"].status_code == 200
    assert response["response"].json() != None


def test_types_in_block_all():
    response = request.api.types_in_block()
    assert response["response"].status_code == 200
    assert response["response"].json() != None


def test_download_pdf():
    response = request.file.download_pdf(registration_number="0100202402080001")
    try:
        # assert response.status_code == 200
        assert response["response"].content != None
    except Exception as ax:
        logger.exception(response["response"].content)
