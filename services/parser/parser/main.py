import json
import random
import requests

from datetime import datetime
from parser.database.database import db

from parser.outgoing_requests.request import request
import parser.utils.utils as utils
from parser.data.deadlines import get_deadlines_data
from parser.data.districts import get_districts_data
from parser.data.regions import get_regions_data
import time


logger = utils.get_logger("main")


# @utils.check_time(logger=logger)
# def get_document_api(code):
#     logger.info(f"Блок {code} начат")

#     req_total_documents = api.publication.documents_for_the_block(code)

#     if insert.get_total_documents(code=code) == req_total_documents["itemsTotalCount"]:
#         logger.info(f"Блок {code} уже заполнен")
#         return

#     req_type = api.publication.type_in_subject(code)

#     for npa in req_type:
#         current_page = 1
#         while True:
#             time.sleep(0.5)
#             print(npa)
#             req = api.publication.documents_on_page_type(
#                 npa_id=npa["id"], block=code, index=current_page
#             )

#             # logger.debug(
#             #     api.publication.documents_on_page_type(
#             #         npa_id=npa["id"], block=code, index=str(current_page)
#             #     )
#             # )
#             if (
#                 insert.get_total_documents_type(code=code, npa_id=npa["id"])
#                 == req["itemsTotalCount"]
#             ):
#                 break

#             if current_page <= req["pagesTotalCount"]:
#                 complex_names: list = []
#                 eo_numbers: list = []
#                 pages_counts: list = []
#                 view_dates: list = []
#                 id_regs: list = []
#                 id_acts: list = []
#                 id_reg = insert.get_id_reg(code=code)
#                 id_act = insert.get_id_act(npa_id=npa["id"])

#                 for item in req["items"]:
#                     complex_names.append(item["complexName"])
#                     eo_numbers.append(item["eoNumber"])
#                     pages_counts.append(item["pagesCount"])
#                     view_dates.append(
#                         datetime.strptime(item["viewDate"], "%d.%m.%Y").strftime(
#                             "%Y-%m-%d"
#                         )
#                     )
#                     id_regs.append(id_reg)
#                     id_acts.append(id_act)
#                 insert.insert_document(
#                     complex_names,
#                     eo_numbers,
#                     pages_counts,
#                     view_dates,
#                     id_regs,
#                     id_acts,
#                 )
#                 current_page += 1

#             elif current_page > req["pagesTotalCount"] or req["pagesTotalCount"] == 0:
#                 break
#     logger.info(f"Блок {code} закончен")


def get_all_types() -> list:

    response = request.api.types_in_block()
    all_types: list = []

    for type in response["response"].json():
        all_types.append({"name": type["name"], "external_id": type["id"]})

    print(json.dumps(all_types[0], ensure_ascii=False, indent=4))
    logger.debug(json.dumps(all_types[0], indent=4, ensure_ascii=False))
    return all_types


def get_subblocks_public_blocks(parent) -> list:
    response = request.api.public_blocks(parent=parent)
    subblocks: list = []

    for subblock in response["response"].json():
        subblocks.append(
            {
                "name": subblock["name"],
                "short_name": subblock["shortName"],
                "external_id": subblock["id"],
                "code": subblock["code"],
                "has_children": subblock["hasChildren"],
                "parent_id": subblock["parentId"],
                "categories": subblock["categories"],
            }
        )

    print(json.dumps(subblocks[0], ensure_ascii=False, indent=4))
    logger.debug(json.dumps(subblocks, indent=4, ensure_ascii=False))
    return subblocks


def get_public_blocks() -> list:
    response = request.api.public_blocks()
    blocks: list = []

    for block in response["response"].json():
        blocks.append(
            {
                "name": block["name"],
                "short_name": block["shortName"],
                "external_id": block["id"],
                "code": block["code"],
                "has_children": block["hasChildren"],
                "parent_id": block["parentId"],
                "categories": block["categories"],
            }
        )

    print(json.dumps(blocks[0], ensure_ascii=False, indent=4))
    logger.debug(json.dumps(blocks, indent=4, ensure_ascii=False))
    return blocks


def main():
    logger.info("Начало работы скрипта")

    # block 1
    db.initiate.create.table_districts()
    db.initiate.create.table_regions()
    db.initiate.create.table_deadlines()
    db.initiate.create.table_receiving_authorities()
    db.initiate.create.table_blocks()
    db.initiate.create.table_document_types()
    db.initiate.create.table_document_types__blocks()
    db.initiate.create.table_documents()

    db.initiate.create.table_roles()
    db.initiate.create.table_users()

    db.initiate.create.index_all()

    # block 2
    db.initiate.insert.table_districts(json_data=get_districts_data())
    db.initiate.insert.table_deadlines(deadlines=get_deadlines_data())

    # block 3

    public_blocks = get_public_blocks()

    all_public_blocks = []
    for public_block in public_blocks:

        if public_block["has_children"] == True:
            subblocks = get_subblocks_public_blocks(parent=public_block["code"])

            for subblock in subblocks:
                all_public_blocks.append(subblock)
        else:
            all_public_blocks.append(public_block)

    db.initiate.insert.table_receiving_authorities(all_public_blocks)

    # block 4

    regions = get_subblocks_public_blocks(parent="subjects")
    logger.info("Заполнение завершено!")


if __name__ == "__main__":
    main()
