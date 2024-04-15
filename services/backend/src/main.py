from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.routers import all_routers
from parser.external_api.request import request

from schemas.deadlines import DeadlinesSchema
from schemas.districts import DistrictSchema
from schemas.regions import RegionSchema
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
        districts_data = [
            DistrictSchema(**district) for district in get_districts_data()
        ]
        deadlines_data = [
            DeadlinesSchema(**deadline) for deadline in get_deadlines_data()
        ]
        regions_data = [RegionSchema(**region) for region in get_regions_data()]
    except Exception as e:
        parser_logger.error(f"Error fetching data: {str(e)}")
        return

    try:
        # Insert Districts
        flag, error = await service.districts.insert_districts(districts=districts_data)

        if not flag:
            raise DataInsertionError(f"При вставке округов произошла ошибка {status}")
        parser_logger.info("Вставка округов прошла успешно")

        # Insert Deadlines
        flag, error = await service.deadlines.insert_deadlines(deadlines=deadlines_data)

        if not flag:
            raise DataInsertionError(f"При вставке дедлайнов произошла ошибка {status}")
        parser_logger.info("Вставка дедлайнов прошла успешно")

    except DataInsertionError as e:
        parser_logger.critical(str(e))
        parser_logger.critical("Выполнение задачи по расписанию оборвалось")
        return

    print(request.api.public_blocks()["response"].json())
    parser_logger.info("Выполнение задачи по расписанию завершено")


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
