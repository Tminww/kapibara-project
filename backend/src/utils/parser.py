from pydantic import BaseModel
from src.errors import DataInsertionError
from src.schemas.base import BaseSchema
from src.schemas.blocks import BlockSchema, OrganInBlockSchema, RegionInBlockSchema
from src.schemas.deadlines import DeadlinesSchema
from src.schemas.districts import DistrictSchema
from src.schemas.regions import MockRegionSchema
from src.services.service import Service
from src.utils.utils import get_logger
from src.external.external import pravo_gov
from src.schemas.deadlines import DeadlinesSchema
from src.schemas.districts import DistrictSchema
from src.schemas.types import PravoGovDocumentTypesSchema
from src.schemas.regions import MockRegionSchema, PravoGovRegionSchema, RegionSchema
from src.schemas.organs import OrganSchema
from src.services.service import Service

from src.assets.data import (
    get_deadlines_data,
    get_districts_data,
    get_regions_data,
)

import json
from typing import List

parser_logger = get_logger(logger_name="repeat_task", file_name="parser")


async def parse():
    parser_logger.info("Выполняется задача по расписанию")
    print("Выполняется задача по расписанию")
    service: Service = Service()

    # Fetch data
    try:
        mock_districts_data: List[DistrictSchema] = [
            DistrictSchema(**district) for district in get_districts_data()
        ]

        mock_deadlines_data: List[DeadlinesSchema] = [
            DeadlinesSchema(**deadline) for deadline in get_deadlines_data()
        ]
        mock_regions_data: List[MockRegionSchema] = [
            MockRegionSchema(**region) for region in get_regions_data()
        ]
    except Exception as e:
        parser_logger.error(f"Error fetching data: {str(e)}")
        return

    try:
        # Insert Districts
        flag, error = await service.districts.insert_districts(
            districts=mock_districts_data
        )

        if not flag:
            raise DataInsertionError(f"При вставке округов произошла ошибка {error}")
        parser_logger.info("Вставка/обновление округов прошла успешно")

        # Insert Deadlines
        flag, error = await service.deadlines.insert_deadlines(
            deadlines=mock_deadlines_data
        )

        if not flag:
            raise DataInsertionError(f"При вставке дедлайнов произошла ошибка {error}")
        parser_logger.info("Вставка/обновление дедлайнов прошла успешно")

    except DataInsertionError as e:
        parser_logger.critical(str(e))
        parser_logger.critical("Выполнение задачи по расписанию оборвалось")
        return

    # Get public blocks
    public_blocks = get_public_blocks()

    all_public_blocks = []
    for public_block in public_blocks:

        if public_block["has_children"] == True:

            subblocks = get_subblocks_public_blocks(parent=public_block["code"])

            for subblock in subblocks:
                all_public_blocks.append(subblock)
        else:
            all_public_blocks.append(public_block)

    public_blocks_data = [OrganSchema(**organ, id=None) for organ in all_public_blocks]
    # parser_logger.debug(public_blocks_data[0].model_dump_json)

    public_blocks_with_inner_id_data = add_id_to_object_in_array(public_blocks_data)

    try:
        # Insert Organs
        flag, error = await service.organs.insert_organs(
            organs=public_blocks_with_inner_id_data
        )

        if not flag:
            raise DataInsertionError(f"При вставке органов произошла ошибка {error}")
        parser_logger.info(
            "Вставка/обновление органов прошла успешно",
        )

    except DataInsertionError as e:
        parser_logger.critical(str(e))
        parser_logger.critical("Выполнение задачи по расписанию оборвалось")
        return

    pravo_gov_regions_data: List[PravoGovRegionSchema] = [
        PravoGovRegionSchema(**region)
        for region in get_subblocks_public_blocks(parent="subjects")
    ]

    status, error = compare_regions(
        api_regions=pravo_gov_regions_data, mock_regions=mock_regions_data
    )
    if not status:
        parser_logger.critical(f"Критическая ошибка! Обновите базу регионов. {error}")
        parser_logger.critical("Выполнение задачи по расписанию оборвалось")
        return

    regions_data = combine_pydantic_list_models(
        mock_regions=mock_regions_data, pravo_gov_regions=pravo_gov_regions_data
    )

    regions_with_inner_id_data = add_id_to_object_in_array(regions_data)

    try:

        # Insert Regions
        flag, error = await service.regions.insert_regions(
            regions=regions_with_inner_id_data
        )

        if not flag:
            raise DataInsertionError(f"При вставке регионов произошла ошибка {error}")
        parser_logger.info(
            "Вставка/обновление регионов прошла успешно",
        )

    except DataInsertionError as e:
        parser_logger.critical(str(e))
        parser_logger.critical("Выполнение задачи по расписанию оборвалось")
        return

    try:
        types_data = get_all_types()
        types_with_inner_id_data = add_id_to_object_in_array(types_data)
        # parser_logger.debug(types_data)

        # Insert Document Types
        flag, error = await service.document_types.insert_types(
            types_with_inner_id_data
        )

        if not flag:
            raise DataInsertionError(
                f"При вставке типов докуметов произошла ошибка {error}"
            )
        parser_logger.info(
            "Вставка/обновление типов документов прошла успешно",
        )

    except DataInsertionError as e:
        parser_logger.critical(str(e))
        parser_logger.critical("Выполнение задачи по расписанию оборвалось")
        return

    # print(public_blocks_data)

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!FIX

    print("Начинается вставка блоков")
    blocks_data: List[BlockSchema] = []

    for public_block in public_blocks_with_inner_id_data:
        print(public_block)
        # ОГВ Субъектов РФ - 022fd55f-9f60-481e-a636-56d74b9ca759 ( А вдруг переименуются )
        if public_block.external_id == "022fd55f-9f60-481e-a636-56d74b9ca759":
            for region in regions_with_inner_id_data:
                print(region)

                blocks_data.append(
                    BlockSchema(
                        organ=OrganInBlockSchema(
                            external_id=public_block.external_id,
                            name=public_block.name,
                            id=public_block.id,
                        ),
                        region=RegionInBlockSchema(
                            external_id=region.external_id,
                            name=region.name,
                            id=region.id,
                        ),
                        id=None,
                    )
                )
                print(blocks_data)

        else:
            print("Нет регионов")
            blocks_data.append(
                BlockSchema(
                    organ=OrganInBlockSchema(
                        external_id=public_block.external_id,
                        name=public_block.name,
                        id=public_block.id,
                    ),
                    region=None,
                    id=None,
                )
            )
            print(blocks_data)

    for data in blocks_data:
        print(data.model_dump_json())

    blocks_with_inner_id_data = add_id_to_object_in_array(blocks_data)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    try:
        # Insert Blocks
        flag, error = await service.blocks.insert_blocks(
            blocks=blocks_with_inner_id_data
        )

        if not flag:
            raise DataInsertionError(f"При вставке блоков произошла ошибка {error}")
        parser_logger.info("Вставка/обновление блоков прошла успешно")

    except DataInsertionError as e:
        parser_logger.critical(str(e))
        parser_logger.critical("Выполнение задачи по расписанию оборвалось")
        return

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # parser_logger.info(f"ALL_TYPES {map(lambda x: x.model_dump, all_types)}")
    # db.initiate.insert.table_document_types(types=all_types)

    # db.initiate.insert.table_regions(blocks=api_regions)
    # db.initiate.update.table_regions(mock_data=mock_regions)

    # db.initiate.insert.table_organ(all_public_blocks)
    parser_logger.info("Выполнение задачи по расписанию завершено")


# def load_districts_from_json() -> List[DistrictSchema] | None:
#     try:
#         mock_districts_data: List[DistrictSchema] = [
#             DistrictSchema(**district) for district in get_districts_data()
#         ]
#         return mock_districts_data
#     except Exception as e:
#         parser_logger.error(f"Ошибка получения данных округов: {str(e)}")
#         return


# def load_deadlines_from_json() -> List[DeadlinesSchema] | None:
#     try:
#         mock_deadlines_data: List[DeadlinesSchema] = [
#             DeadlinesSchema(**deadline) for deadline in get_deadlines_data()
#         ]

#         return mock_deadlines_data
#     except Exception as e:
#         parser_logger.error(f"Ошибка получения данных дедлайнов: {str(e)}")
#         return


# def load_regions_from_json() -> List[MockRegionSchema] | None:
#     try:
#         mock_regions_data: List[MockRegionSchema] = [
#             MockRegionSchema(**region) for region in get_regions_data()
#         ]
#         return mock_regions_data
#     except Exception as e:
#         parser_logger.error(f"Ошибка получения данных регионов: {str(e)}")
#         return


# def insert_districts():
#     pass


def add_id_to_object_in_array(
    array: List[BaseSchema], inner_id_start_value: int = 1
) -> dict:
    for object in array:
        object.id = inner_id_start_value
        inner_id_start_value += 1
    return array


def get_block_types(block: str) -> list:

    response = pravo_gov.api.types_in_block(block=block)
    block_types: list = []

    for type in json.loads(response.content):
        block_types.append(
            dict(
                name=type["name"],
                external_id=type["id"],
                # FIXME: ЭТО КОСТЫЛЬ
                # id_dl=1,
            )
        )

    # print(json.dumps(block_types[0], ensure_ascii=False, indent=4))
    parser_logger.debug(json.dumps(block_types[0], indent=4, ensure_ascii=False))
    return block_types


def get_subblocks_public_blocks(parent) -> list:
    response = pravo_gov.api.public_blocks(parent=parent)
    subblocks: list = []

    for subblock in json.loads(response.content):
        subblocks.append(
            dict(
                name=subblock["name"],
                short_name=subblock["shortName"],
                external_id=subblock["id"],
                code=subblock["code"],
                has_children=subblock["hasChildren"],
                parent_id=subblock["parentId"],
                categories=subblock["categories"],
            )
        )

    return subblocks


def get_public_blocks() -> list:
    response = pravo_gov.api.public_blocks()
    blocks: list = []

    for block in json.loads(response.content):
        blocks.append(
            dict(
                name=block["name"],
                short_name=block["shortName"],
                external_id=block["id"],
                code=block["code"],
                has_children=block["hasChildren"],
                parent_id=block["parentId"],
                categories=block["categories"],
            )
        )

    return blocks


def compare_regions(
    mock_regions: List[MockRegionSchema], api_regions: List[PravoGovRegionSchema]
) -> tuple[bool, str | None]:

    mock_regions_name = [region.name for region in mock_regions]
    for region in api_regions:
        if region.name not in mock_regions_name:
            error = region.name
            return (False, error)

    return (True, None)


# Функция для объединения списков моделей
def combine_pydantic_list_models(
    mock_regions: List[MockRegionSchema], pravo_gov_regions: List[PravoGovRegionSchema]
) -> List[RegionSchema]:
    combined_list = []

    for mock_region in mock_regions:
        for pravo_gov_region in pravo_gov_regions:
            if mock_region.name == pravo_gov_region.name:
                combined_list.append(
                    RegionSchema(
                        id=None,
                        name=pravo_gov_region.name,
                        short_name=pravo_gov_region.short_name,
                        code=pravo_gov_region.code,
                        external_id=pravo_gov_region.external_id,
                        parent_id=pravo_gov_region.parent_id,
                        id_dist=mock_region.id_dist,
                    )
                )
                break
    return combined_list


def get_all_types() -> list[PravoGovDocumentTypesSchema]:

    response = pravo_gov.api.types_in_block()

    all_types: list = []

    for type in json.loads(response.content):
        all_types.append(
            PravoGovDocumentTypesSchema(
                id=None,
                name=type["name"],
                external_id=type["id"],
            )
        )

    return all_types
