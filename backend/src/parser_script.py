from parser.service.api_service import ApiService as api_service

from parser.database.database import db
from parser.assets.deadlines.data import get_deadlines_data
from parser.assets.districts.data import get_districts_data
from parser.assets.regions.data import get_regions_data
import time
from utils import utils

logger = utils.get_logger("parser")


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


def main():
    logger.info("Начало работы скрипта")
    # block 1 create table index

    # db.initiate.create.table_districts()
    # db.initiate.create.table_regions()
    # db.initiate.create.table_deadlines()
    # db.initiate.create.table_organ()
    # db.initiate.create.table_blocks()
    # db.initiate.create.table_document_types()
    # db.initiate.create.table_document_types__blocks()
    # db.initiate.create.table_documents()

    # db.initiate.create.table_roles()
    # db.initiate.create.table_users()

    # db.initiate.create.index_all()

    # block 2 districts deadlines

    db.initiate.insert.table_districts(districts=get_districts_data())
    db.initiate.insert.table_deadlines(deadlines=get_deadlines_data())

    # block 3 organ

    public_blocks = api_service.get_public_blocks()

    all_public_blocks = []
    for public_block in public_blocks:

        if public_block["has_children"] == True:
            subblocks = api_service.get_subblocks_public_blocks(
                parent=public_block["code"]
            )

            for subblock in subblocks:
                all_public_blocks.append(subblock)
        else:
            all_public_blocks.append(public_block)

    db.initiate.insert.table_organ(all_public_blocks)

    # block 4 regions

    api_regions = api_service.get_subblocks_public_blocks(parent="subjects")
    mock_regions = get_regions_data()

    status, error = utils.compare_regions(
        api_regions=api_regions, mock_regions=mock_regions
    )
    if not status:
        logger.critical(f"Критическая ошибка! Обновите базу регионов. {error}")
        return

    db.initiate.insert.table_regions(blocks=api_regions)
    db.initiate.update.table_regions(mock_data=mock_regions)

    # block 5 documents_types КОСТЫЛЬНО

    all_types = api_service.get_all_types()
    db.initiate.insert.table_document_types(types=all_types)

    # block 6 blocks (reciving_  regions)
    print(all_public_blocks)

    for block in all_public_blocks:
        block_types = api_service.get_block_types(block=block["code"])

    logger.info("Заполнение завершено!")


if __name__ == "__main__":
    main()
