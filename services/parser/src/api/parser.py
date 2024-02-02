def get_blocks():
    """возвращает все необходимые блоки для работы парсера

    Returns:
        str: возвращает api по которому будет идти обращение

    Example:
        [
            {
                "shortName":"Президент Российской Федерации",
                "menuName":"Президент Российской Федерации",
                "code":"president",
                "description":"Законы Российской Федерации о поправке к  Конституции Российской Федерации,\nфедеральные конституционные законы,\nфедеральные законы,\nуказы Президента Российской Федерации,\nраспоряжения Президента Российской Федерации",
                "weight":1000,
                "isBlocked":false,
                "parent":null,
                "section":null,
                "parentId":null,
                "hasChildren":false,
                "isAgenciesOfStateAuthorities":false,
                "items":[],
                "imageId":"11f3a3c0-3cbc-4748-85e1-0df692e7138e",
                "categories":null,
                "treeViewParentId":null,
                "name":"Президент Российской Федерации",
                "id":"e94b6872-dcac-414f-b2f1-a538d13a12a0"
            },
            {
                "shortName":"Федеральное Собрание Российской Федерации",
                "menuName":"Федеральное Собрание Российской Федерации",
                "code":"assembly",
                "description":"Акты палат Федерального Собрания, принятые по вопросам, отнесенным к ведению палат частью 1 статьи 102 и частью 1 статьи 103 Конституции Российской Федерации",
                "weight":998,"isBlocked":false,
                "parent":null,
                "section":null,
                "parentId":null,
                "hasChildren":true,
                "isAgenciesOfStateAuthorities":false,
                "items":[
                    {
                        "shortName":"Совет Федерации ФС РФ",
                        "menuName":"Совет Федерации ФС РФ",
                        "code":"council_1",
                        "description":"Постановления Совета Федерации, принятые по вопросам, \r\nотнесенным к ведению палаты частью 1 статьи 102 \r\nКонституции Российской Федерации",
                        "weight":999,
                        "isBlocked":false,
                        "parent":null,
                        "section":null,
                        "parentId":"a30c9c82-4a21-48ab-a41d-d1891a10962c",
                        "hasChildren":false,
                        "isAgenciesOfStateAuthorities":false,
                        "items":[],
                        "imageId":"bef4c47c-65c4-41f8-8d3b-b3f5f44eaf16",
                        "categories":null,
                        "treeViewParentId":null,
                        "name":"Совет Федерации Федерального  Собрания Российской Федерации",
                        "id":"950cdcb1-f55d-4e22-9f05-87074fe08efd"
                    },
                    {
                        "shortName":"Государственная Дума ФС РФ",
                        "menuName":"Государственная Дума ФС РФ",
                        "code":"council_2",
                        "description":"Постановления Государственной Думы, принятые по вопросам, \r\nотнесенным к ведению палаты частью 1 статьи 103 \r\nКонституции Российской Федерации",
                        "weight":998,
                        "isBlocked":false,
                        "parent":null,
                        "section":null,
                        "parentId":"a30c9c82-4a21-48ab-a41d-d1891a10962c",
                        "hasChildren":false,
                        "isAgenciesOfStateAuthorities":false,
                        "items":[],
                        "imageId":"13428305-e992-4611-a89e-a478b6eeb917",
                        "categories":null,
                        "treeViewParentId":null,
                        "name":"Государственная Дума Федерального Собрания Российской Федерации",
                        "id":"0dbe1bc1-0e40-446a-a3ba-1ccabe18ca5e"
                    }
                ],"
                imageId":null,
                "categories":null,
                "treeViewParentId":null,
                "name":"Федеральное Собрание Российской Федерации",
                "id":"a30c9c82-4a21-48ab-a41d-d1891a10962c"
            }
        ]
    """
    return f"http://publication.pravo.gov.ru/api/PublicBlocks/?Categories"


def get_documents_on_page(code):
    """Получение документов для первой страницы заданного блока

    Args:
        code (_type_): название блока

    Returns:
        str: возвращает api по которому будет идти обращение
    """
    return f"http://publication.pravo.gov.ru/api/Documents?block={code}&PageSize=200&Index=1"


def get_documents_on_page_type(npa_id, code, index):
    return f"http://publication.pravo.gov.ru/api/Documents?DocumentTypes={npa_id}&block={code}&PageSize=200&Index={index}"


def get_subjects():
    return "http://publication.pravo.gov.ru/api/PublicBlocks/?parent=subjects"


def get_type_all():
    return "http://publication.pravo.gov.ru/api/DocumentTypes"


def get_type_in_subject(code):
    return f"http://publication.pravo.gov.ru/api/DocumentTypes?block={code}"
