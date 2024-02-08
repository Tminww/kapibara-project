import random
import requests

from datetime import datetime

import parser.database.initial as initial
import parser.database.query as query

# import services.parser.parser.api.publication.publication as request_api
from parser.api.api import api
import parser.utils.utils as utils

import time
import parser.utils.utils as utils


logger = utils.get_logger("main")


@utils.check_time(logger=logger)
def get_document_api(code):
    logger.info(f"Блок {code} начат")

    req_total_documents = api.publication.documents_on_page(code)

    if query.get_total_documents(code=code) == req_total_documents["itemsTotalCount"]:
        logger.info(f"Блок {code} уже заполнен")
        return

    req_type = api.publication.type_in_subject(code)

    for npa in req_type:
        current_page = 1
        while True:
            time.sleep(0.5)
            print(npa)
            req = api.publication.documents_on_page_type(
                npa_id=npa["id"], block=code, index=current_page
            )

            # logger.debug(
            #     api.publication.documents_on_page_type(
            #         npa_id=npa["id"], block=code, index=str(current_page)
            #     )
            # )
            if (
                query.get_total_documents_type(code=code, npa_id=npa["id"])
                == req["itemsTotalCount"]
            ):
                break

            if current_page <= req["pagesTotalCount"]:
                complex_names: list = []
                eo_numbers: list = []
                pages_counts: list = []
                view_dates: list = []
                id_regs: list = []
                id_acts: list = []
                id_reg = query.get_id_reg(code=code)
                id_act = query.get_id_act(npa_id=npa["id"])

                for item in req["items"]:
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

            elif current_page > req["pagesTotalCount"] or req["pagesTotalCount"] == 0:
                break
    logger.info(f"Блок {code} закончен")


def get_npa_api() -> list:
    names: list = []
    npa_id: list = []
    req = api.publication.type_all()

    for npa in req:
        names.append(npa["name"])
        npa_id.append(npa["id"])
    # logger.debug(list(zip(names, npa_id)))
    return list(zip(names, npa_id))


def get_subject_api() -> list:
    req = api.publication.subjects()
    names: list = []
    codes: list = []
    for subject in req:
        names.append(subject["name"])
        codes.append(subject["code"])
    # logger.debug(list(zip(names, codes)))
    return list(zip(names, codes))


@utils.retry_request(logger=logger)
def test():

    response = requests.get(url="https://api.tminww.site/subjects")

    if response.status_code != 200:
        raise requests.exceptions.RequestException
    else:
        return response


def main():
    logger.info("Начало работы скрипта")

    test()

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
