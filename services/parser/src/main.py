import requests

from datetime import datetime

import database.initial as initial
import database.query as query
import api.parser as parser
import utils.utils as utils

from log.createLogger import get_logger
import time

logger = get_logger("main")


@utils.check_time
def get_document_api(code):
    logger.info(f"Блок {code} начат")

    req_total_documents = requests.get(
        url=parser.get_documents_on_page(code),
    )

    if (
        query.get_total_documents(code=code)
        == req_total_documents.json()["itemsTotalCount"]
    ):
        logger.info(f"Блок {code} уже заполнен")
        return

    req_type = requests.get(
        url=parser.get_type_in_subject(code),
    )
    for npa in req_type.json():
        current_page = 1
        while True:
            time.sleep(0.5)
            req = requests.get(
                url=parser.get_documents_on_page_type(
                    npa_id=npa["id"], code=code, index=str(current_page)
                )
            )
            logger.debug(
                parser.get_documents_on_page_type(
                    npa_id=npa["id"], code=code, index=str(current_page)
                )
            )
            if (
                query.get_total_documents_type(code=code, npa_id=npa["id"])
                == req.json()["itemsTotalCount"]
            ):
                break

            if current_page <= req.json()["pagesTotalCount"]:
                complex_names: list = []
                eo_numbers: list = []
                pages_counts: list = []
                view_dates: list = []
                id_regs: list = []
                id_acts: list = []
                id_reg = query.get_id_reg(code=code)
                id_act = query.get_id_act(npa_id=npa["id"])

                for item in req.json()["items"]:
                    complex_names.append(item["complexName"])
                    eo_numbers.append(item["eoNumber"])
                    pages_counts.append(item["pagesCount"])
                    view_dates.append(
                        datetime.strptime(item["viewDate"], "%d.%m.%Y").strftime(
                            "%Y-%m-%d"
                        )
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

            elif (
                current_page > req.json()["pagesTotalCount"]
                or req.json()["pagesTotalCount"] == 0
            ):
                break
    logger.info(f"Блок {code} закончен")


def get_npa_api() -> list:
    names: list = []
    npa_id: list = []
    req = requests.get(url=parser.get_type_all())

    for npa in req.json():
        names.append(npa["name"])
        npa_id.append(npa["id"])
    logger.debug(list(zip(names, npa_id)))
    return list(zip(names, npa_id))


def get_subject_api() -> list:
    req = requests.get(url=parser.get_subjects())
    names: list = []
    codes: list = []
    for subject in req.json():
        names.append(subject["name"])
        codes.append(subject["code"])
    logger.debug(list(zip(names, codes)))
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

    logger.info("Заполнение завершено!")


if __name__ == "__main__":
    main()
