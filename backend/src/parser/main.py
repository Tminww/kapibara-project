import asyncio
import time
from pydantic import BaseModel
from src.errors import DataInsertionError
from src.schemas.base import BaseSchema
from src.schemas.blocks import BlockSchema, OrganInBlockSchema, RegionInBlockSchema
from src.schemas.deadlines import DeadlinesSchema
from src.schemas.districts import DistrictSchema
from src.schemas.regions import MockRegionSchema
from src.services.service import Service
from src.utils.utils import check_time, parser_logger
from src.parser.external_api.external import pravo_gov
from src.schemas.deadlines import DeadlinesSchema
from src.schemas.districts import DistrictSchema
from src.schemas.types import PravoGovDocumentTypesSchema, TypesInBlockSchema
from src.schemas.regions import MockRegionSchema, PravoGovRegionSchema, RegionSchema
from src.schemas.organs import OrganSchema
from src.services.service import Service

from src.parser.assets.data import (
    get_deadlines_data,
    get_districts_data,
    get_regions_data,
)

import json
from typing import List

service: Service = Service()


async def parse():

    parser_logger.info("\n\n\nВыполняется задача по расписанию\n\n")

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
    public_blocks = await get_public_blocks()

    all_public_blocks = []
    for public_block in public_blocks:

        if public_block["has_children"] == True:

            subblocks = await get_subblocks_public_blocks(parent=public_block["code"])

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
        for region in await get_subblocks_public_blocks(parent="subjects")
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
    # print(regions_data)

    regions_with_inner_id_data = add_id_to_object_in_array(regions_data)
    # print(regions_with_inner_id_data)
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
        types_data = await get_all_types()
        types_with_inner_id_data: List[PravoGovDocumentTypesSchema] = (
            add_id_to_object_in_array(types_data)
        )
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

    # print("Начинается вставка блоков")
    blocks_data: List[BlockSchema] = []
    # print(public_blocks_with_inner_id_data)
    for public_block in public_blocks_with_inner_id_data:
        # ОГВ Субъектов РФ - 022fd55f-9f60-481e-a636-56d74b9ca759 ( А вдруг переименуются )
        if public_block.external_id == "022fd55f-9f60-481e-a636-56d74b9ca759":
            for region in regions_with_inner_id_data:
                # print(region)
                blocks_data.append(
                    BlockSchema(
                        organ=OrganInBlockSchema(
                            external_id=public_block.external_id,
                            name=public_block.name,
                            id=public_block.id,
                            code=public_block.code,
                        ),
                        region=RegionInBlockSchema(
                            external_id=region.external_id,
                            name=region.name,
                            id=region.id,
                            code=region.code,
                        ),
                        id=None,
                    )
                )
                # print(blocks_data)

        else:
            # print("Нет регионов")
            blocks_data.append(
                BlockSchema(
                    organ=OrganInBlockSchema(
                        external_id=public_block.external_id,
                        name=public_block.name,
                        id=public_block.id,
                        code=public_block.code,
                    ),
                    region=None,
                    id=None,
                )
            )
            # print(blocks_data)

    blocks_with_inner_id_data: List[BlockSchema] = add_id_to_object_in_array(
        blocks_data
    )
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
    ## Вставка типов блоков

    # parser_logger.debug(blocks_with_inner_id_data)
    # parser_logger.debug(types_with_inner_id_data)

    types_in_block: List[TypesInBlockSchema] = []
    counter_for_id: int = 1
    for block in blocks_with_inner_id_data:

        if block.region:
            types = await get_types_in_block(
                block=block.region.code,
                types_with_inner_id_data=types_with_inner_id_data,
            )

            for type in types:
                types_in_block.append(
                    TypesInBlockSchema(
                        id=counter_for_id,
                        block=block,
                        type=type,
                    )
                )
                counter_for_id += 1

        else:
            types = await get_types_in_block(
                block=block.organ.code,
                types_with_inner_id_data=types_with_inner_id_data,
            )

            for type in types:
                types_in_block.append(
                    TypesInBlockSchema(
                        id=counter_for_id,
                        block=block,
                        type=type,
                    )
                )
                counter_for_id += 1

    try:
        # Insert Types in Block
        flag, error = await service.types_in_block.insert_types_in_block(
            types_in_block=types_in_block
        )

        if not flag:
            raise DataInsertionError(
                f"При вставке типов блоков произошла ошибка {error}"
            )
        parser_logger.info("Вставка/обновление типов блоков прошла успешно")

    except DataInsertionError as e:
        parser_logger.critical(str(e))
        parser_logger.critical("Выполнение задачи по расписанию оборвалось")
        return

    # ВСТАВКА ДОКУМЕНТОВ В БАЗУ
    print("ВСТАВКА ДОКУМЕНТОВ В БАЗУ")
    parser_logger.info("ВСТАВКА ДОКУМЕНТОВ В БАЗУ Данных")

    for type_in_block in types_in_block:

        if type_in_block.block.region:
            await get_documents_in_block_api(
                type_in_block.id,
                type_in_block.block.region.code,
                type_in_block.type.external_id,
            )

        else:
            await get_documents_in_block_api(
                type_in_block.id,
                type_in_block.block.organ.code,
                type_in_block.type.external_id,
            )

    parser_logger.info("Выполнение задачи по расписанию завершено")


@check_time(logger=parser_logger)
async def get_documents_in_block_api(block_type_id, block_code, type_external_id):
    print(block_type_id, block_code, type_external_id)
    parser_logger.info(f"Блок {block_type_id} {block_code} начат")

    document_count_api: int = await get_document_count_api(block_code, type_external_id)
    print("Document Count API", document_count_api)

    document_count_db: int = await get_document_count_db(block_type_id)
    print("Document Count DB", document_count_db)

    if document_count_api == 0:
        parser_logger.info(f"Блок {block_code} пуст")
        return
    
    if document_count_api == document_count_db:
        parser_logger.info(f"Блок {block_code} уже заполнен")
        return

    documents: List[dict] = []

    current_page = 1
    while True:
        print("Current Page", current_page)
        time.sleep(0.5)
        response = await get_documents_api(block_code, type_external_id, current_page)

        documents.extend(response.get("items"))
        print("Pages Total Count", response["pagesTotalCount"], "Current Page", current_page)
        if response.get("pagesTotalCount") == current_page:
            print("break")
            break
        
        current_page += 1

    # print("Documents", documents)

    try:
        # Insert Documents
        flag, error = await insert_documents_in_db(
            documents=documents, block_type_id=block_type_id
        )
        print(flag, error)

        if not flag:
            raise DataInsertionError(f"При вставке документов произошла ошибка {error}")
        parser_logger.info(f"Блок {block_type_id} {block_code} завершен")
        return

    except DataInsertionError as e:
        parser_logger.critical(str(e))
        parser_logger.critical("Выполнение задачи по расписанию оборвалось")
        return


async def get_document_count_api(block_code, type_external_id) -> int:
    response = await pravo_gov.api.documents_for_the_block(
        block=block_code, index=1, document_type=type_external_id
    )
    return json.loads(response.content).get("itemsTotalCount", 0)


async def get_documents_api(block_code, type_external_id, current_page) -> dict:
    response = await pravo_gov.api.documents_for_the_block(
        block=block_code, index=current_page, document_type=type_external_id
    )

    return json.loads(response.content)


async def get_document_count_db(block_type_id) -> int:
    response = await service.documents.get_documents_count_in_block(block_type_id)
    return response


async def insert_documents_in_db(documents: List[dict], block_type_id: int)-> tuple[bool, str]:

    flag, status = await service.documents.insert_documents(documents, block_type_id)

    return (flag, status)


def add_id_to_object_in_array(
    array: List[BaseSchema], inner_id_start_value: int = 1
) -> dict:
    for object in array:
        object.id = inner_id_start_value
        inner_id_start_value += 1
    return array


async def get_types_in_block(
    block: str, types_with_inner_id_data: List[PravoGovDocumentTypesSchema]
) -> List[PravoGovDocumentTypesSchema]:

    response = await pravo_gov.api.types_in_block(block=block)
    block_types: List[PravoGovDocumentTypesSchema] = []

    for type in json.loads(response.content):
        for type_with_inner_id in types_with_inner_id_data:
            if type["id"] == type_with_inner_id.external_id:
                block_types.append(
                    PravoGovDocumentTypesSchema(
                        id=type_with_inner_id.id,
                        name=type["name"],
                        external_id=type["id"],
                    )
                )
    # print(block_types)
    # print(json.dumps(block_types[0], ensure_ascii=False, indent=4))
    # parser_logger.debug(json.dumps(block_types[0], indent=4, ensure_ascii=False))
    return block_types


async def get_subblocks_public_blocks(parent) -> list:
    response = await pravo_gov.api.public_blocks(parent=parent)
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


async def get_public_blocks() -> list:
    response = await pravo_gov.api.public_blocks()
    blocks: list = []
    print(response.content)
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


async def get_all_types() -> List[PravoGovDocumentTypesSchema]:

    response = await pravo_gov.api.types_in_block()

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

if __name__ == "__main__":
    asyncio.run(parse())
