import requests
import time
from datetime import datetime

import database.initial as initial
import database.query as query
import api.parser as parser
from log.createLogger import get_logger


logging = get_logger()


def check_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"{func.__name__} Всего времени {end_time - start_time}")
        return res

    return wrapper


@check_time
def get_document_api(code):
    logging.info(f"Регион {code} начат")
    print(f"Регион {code} начат")

    # Запрос общего количества документов
    req_total_documents = requests.get(url=parser.get_documents_on_page(code))

    # Проверка статуса ответа
    if req_total_documents.status_code != 200:
        logging.error(f"Ошибка при запросе: статус {req_total_documents.status_code}")
        return

    # Попытка парсинга JSON
    try:
        total_documents_data = req_total_documents.json()
    except ValueError as e:
        logging.error(f"Ошибка при парсинге JSON: {e}")
        return

    # Проверка, нужно ли обновлять данные
    if query.get_total_documents(code=code) == total_documents_data.get("itemsTotalCount"):
        logging.info(f"Регион {code} уже заполнен")
        print(f"Регион {code} уже заполнен")
        return

    # Запрос типов документов
    req_type = requests.get(url=parser.get_type_in_subject(code))

    # Проверка статуса ответа
    if req_type.status_code != 200:
        logging.error(f"Ошибка при запросе типов документов: статус {req_type.status_code}")
        return

    # Попытка парсинга JSON
    try:
        type_data = req_type.json()
    except ValueError as e:
        logging.error(f"Ошибка при парсинге JSON типов документов: {e}")
        return

    # Обработка каждого типа документа
    for npa in type_data:
        current_page = 1
        while True:
            time.sleep(0.5)
            req = requests.get(
                url=parser.get_documents_on_page_type(
                    npa_id=npa["id"], code=code, index=str(current_page)
                )
            )

            # Проверка статуса ответа
            if req.status_code != 200:
                logging.error(f"Ошибка при запросе документов: статус {req.status_code}")
                break

            # Попытка парсинга JSON
            try:
                documents_data = req.json()
            except ValueError as e:
                logging.error(f"Ошибка при парсинге JSON документов: {e}")
                break

            # Проверка, нужно ли обновлять данные
            if query.get_total_documents_type(code=code, npa_id=npa["id"]) == documents_data.get("itemsTotalCount"):
                break

            if current_page <= documents_data.get("pagesTotalCount", 0):
                complex_names = []
                eo_numbers = []
                pages_counts = []
                view_dates = []
                id_regs = []
                id_acts = []
                id_reg = query.get_id_reg(code=code)
                id_act = query.get_id_act(npa_id=npa["id"])

                for item in documents_data.get("items", []):
                    complex_names.append(item.get("complexName"))
                    eo_numbers.append(item.get("eoNumber"))
                    pages_counts.append(item.get("pagesCount"))
                    view_dates.append(
                        datetime.strptime(item.get("viewDate"), "%d.%m.%Y").strftime("%Y-%m-%d")
                    )
                    id_regs.append(id_reg)
                    id_acts.append(id_act)

                query.insert_document(
                    complex_names,
                    eo_numbers,
                    pages_counts,
                    view_dates,
                    id_regs,
                    id_acts,
                )
                current_page += 1
            else:
                break

    logging.info(f"Регион {code} закончен")
    print(f"Регион {code} закончен")

def get_npa_api() -> list:
    names: list = []
    npa_id: list = []
    req = requests.get(url=parser.get_type_all())

    for npa in req.json():
        names.append(npa["name"])
        npa_id.append(npa["id"])
    return list(zip(names, npa_id))


def get_subject_api() -> list:
    req = requests.get(url=parser.get_subjects())
    names: list = []
    codes: list = []
    for subject in req.json():
        names.append(subject["name"])
        codes.append(subject["code"])
    
    other_codes = [
        "president",
        "council_1",
        "council_2",
        "government",
        "federal_authorities",
        "court",
        "international",
        "un_securitycouncil",
    ]
    
    other_names = [
        'Президент РФ',
        'Совет Федерации Федерального Собрания РФ',
        'Государственная Дума Федерального Собрания РФ',
        'Правительство РФ',
        'ФОИВ и ФГО РФ',
        'Конституционный Суд РФ',
        'Международные договоры РФ',
        'Совет Безопасности ООН',
        
    ]
    
    for name in other_names:
        names.append(name)
    
    for code in other_codes:
        codes.append(code)

    return list(zip(names, codes))


def main():
    print(1234)
    initial.create_tables()
    name_code = get_subject_api()
    name_npa_id = get_npa_api()

    query.insert_act(name_npa_id)
    query.insert_region(name_code)
    query.update_region()

    for name, code in name_code:
        get_document_api(code=code)

    logging.info("Заполнение завершено!")


if __name__ == "__main__":
    main()
