def get_documents_on_page(code):
    return f"http://publication.pravo.gov.ru/api/Documents?block={code}&PageSize=200&Index=1"


def get_documents_on_page_type(npa_id, code, index):
    return f"http://publication.pravo.gov.ru/api/Documents?DocumentTypes={npa_id}&block={code}&PageSize=200&Index={index}"


def get_subjects():
    return "http://publication.pravo.gov.ru/api/PublicBlocks/?parent=subjects"


def get_type_all():
    return "http://publication.pravo.gov.ru/api/DocumentTypes"


def get_type_in_subject(code):
    return f"http://publication.pravo.gov.ru/api/DocumentTypes?block={code}"
