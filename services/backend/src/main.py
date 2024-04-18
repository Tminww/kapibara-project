import json
from typing import List
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.routers import all_routers
from parser.external_api.external import pravo_gov

from schemas.deadlines import DeadlinesSchema
from schemas.districts import DistrictSchema
from schemas.regions import MockRegionSchema, PravoGovRegionSchema, RegionSchema
from schemas.organs import OrganSchema
from services.service import Service
from utils.utils import get_logger
from errors import (
    DataDelitionError,
    DataInsertionError,
    DateValidationError,
    ResultIsEmptyError,
)
from utils.tasks import repeat_every


from parser.assets.deadlines.data import get_deadlines_data
from parser.assets.districts.data import get_districts_data
from parser.assets.regions.data import get_regions_data


backend_logger = get_logger(logger_name="fastapi.main", file_name="backend")
parser_logger = get_logger(logger_name="repeat_task", file_name="parser")


app = FastAPI(title="Вывод статистики по документам")

# Base.metadata.create_all(bind=sync_engine)

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for router in all_routers:
    app.include_router(router)

# Настройка логгера


@app.on_event("startup")
@repeat_every(seconds=60, logger=parser_logger)
async def run_parser():
    """
    Executes a scheduled task that performs parsing and data insertion into a database.

    This function is executed on the startup of a FastAPI application and runs periodically every 60 seconds.
    It performs the following tasks:
    1. Retrieves data from JSON files using utility functions.
    2. Converts the retrieved data into appropriate schema objects.
    3. Inserts the districts data into the database using the `insert_districts` method of the `Service` class.
    4. Logs the success or failure of the districts insertion.
    5. Inserts the deadlines data into the database using the `insert_deadlines` method of the `Service` class.
    6. Logs the success or failure of the deadlines insertion.
    7. Logs a final message indicating the completion of the scheduled task.

    Inputs:
    - app: The FastAPI application instance.
    - parser_logger: The logger object used for logging.

    Outputs:
    None
    """
    parser_logger.info("Выполняется задача по расписанию")

    service: Service = Service()

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
        parser_logger.info("Вставка округов прошла успешно")

        # Insert Deadlines
        flag, error = await service.deadlines.insert_deadlines(
            deadlines=mock_deadlines_data
        )

        if not flag:
            raise DataInsertionError(f"При вставке дедлайнов произошла ошибка {error}")
        parser_logger.info("Вставка дедлайнов прошла успешно")

    except DataInsertionError as e:
        parser_logger.critical(str(e))
        parser_logger.critical("Выполнение задачи по расписанию оборвалось")
        return

    mock_districts_data = [
        DistrictSchema(**district) for district in get_districts_data()
    ]
    public_blocks = get_public_blocks()

    all_public_blocks = []
    for public_block in public_blocks:

        if public_block["has_children"] == True:

            subblocks = get_subblocks_public_blocks(parent=public_block["code"])

            for subblock in subblocks:
                all_public_blocks.append(subblock)
        else:
            all_public_blocks.append(public_block)

    public_blocks_data = [OrganSchema(**organ) for organ in all_public_blocks]
    parser_logger.debug(public_blocks_data[0].model_dump_json)

    try:
        # Insert Organs
        flag, error = await service.organs.insert_organs(organs=public_blocks_data)

        if not flag:
            raise DataInsertionError(f"При вставке органов произошла ошибка {error}")
        parser_logger.info(
            "Вставка органов прошла успешно",
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

    service.regions.insert_regions()
    # db.initiate.insert.table_regions(blocks=api_regions)
    # db.initiate.update.table_regions(mock_data=mock_regions)

    # db.initiate.insert.table_organ(all_public_blocks)
    parser_logger.info("Выполнение задачи по расписанию завершено")


def get_subblocks_public_blocks(parent) -> list:
    response = pravo_gov.api.public_blocks(parent=parent)
    subblocks: list = []

    for subblock in response["response"].json():
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

    print(json.dumps(subblocks[0], ensure_ascii=False, indent=4))
    parser_logger.debug(json.dumps(subblocks[0], indent=4, ensure_ascii=False))
    return subblocks


def get_public_blocks() -> list:
    response = pravo_gov.api.public_blocks()
    blocks: list = []

    for block in response["response"].json():
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

    print(json.dumps(blocks[0], ensure_ascii=False, indent=4))
    parser_logger.debug(json.dumps(blocks[0], indent=4, ensure_ascii=False))
    return blocks


def compare_regions(
    mock_regions: List[MockRegionSchema], api_regions: List[PravoGovRegionSchema]
) -> List[RegionSchema]:

    mock_regions_name = [region.name for region in mock_regions]
    for region in api_regions:
        if region.name not in mock_regions_name:
            error = region.name
            return (False, error)

    # regions_data = [
    #     RegionSchema(**pravo_gov_region.model_dump(), id_dist=) for pravo_gov_region, mock_region in api_regions, mock_regions
    # ]

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


@app.exception_handler(DateValidationError)
async def date_validation_exception_handler(request: Request, e: DateValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": f"Invalid date format ({str(e).splitlines()[2].strip().split(' ')[2]}). Use YYYY-MM-DD."
        },
    )


@app.exception_handler(ResultIsEmptyError)
async def result_is_empty_exception_handler(request: Request, e: ResultIsEmptyError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": str(e),
        },
    )


@app.exception_handler(DataInsertionError)
async def data_insertion_exception_handler(request: Request, e: DataInsertionError):
    error = e.args[0].splitlines()[0].split(":")[-1]
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"An error occurred while inserting: {str(error)}"},
    )


@app.exception_handler(DataDelitionError)
async def data_deletion_exception_handler(request: Request, e: DataDelitionError):
    error = e.args[0].splitlines()[0].split(":")[-1]
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"An error occurred while deleting: {str(error)}"},
    )
