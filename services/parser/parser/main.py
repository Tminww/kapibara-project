import json
import random
import requests

from datetime import datetime

import services.parser.parser.database.initiate as initiate
import parser.database.query as query

# import services.parser.parser.api.publication.publication as request_api
from services.parser.parser.outgoing_requests.request import api
import parser.utils.utils as utils

import time
import parser.utils.utils as utils


logger = utils.get_logger("main")


@utils.check_time(logger=logger)
def get_document_api(code):
    logger.info(f"Блок {code} начат")

    req_total_documents = api.publication.documents_for_the_block(code)

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


def get_all_types() -> list:

    response = api.publication.types_in_block()
    all_types: list = []

    for type in response["response"].json():
        all_types.append({"name": type["name"], "external_id": type["id"]})

    print(json.dumps(all_types[0], ensure_ascii=False, indent=4))
    logger.debug(json.dumps(all_types[0], indent=4, ensure_ascii=False))
    return all_types


def get_subjects() -> list:
    response = api.publication.subblocks(parent="subjects")
    subjects: list = []

    for subject in response["response"].json():
        subjects.append(
            {
                "name": subject["shortName"],
                "short_name": subject["shortName"],
                "external_id": subject["id"],
                "code": subject["code"],
                "parent_id": subject["parentId"],
                "categories": subject["categories"],
            }
        )

    print(json.dumps(subjects[0], ensure_ascii=False, indent=4))
    logger.debug(json.dumps(subjects[0], indent=4, ensure_ascii=False))
    return subjects


def main():
    logger.info("Начало работы скрипта")

    initiate.create_tables()
    subjects = get_subjects()
    all_types = get_all_types()

    query.insert_types(types=all_types)
    query.insert_regions(blocks=subjects)
    query.update_subjects()

    for name, code in name_code:
        get_document_api(code=code)

    logger.info("Заполнение завершено!")


if __name__ == "__main__":
    main()
