from typing import Annotated, List
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from api.routers import all_routers

# from models.base import Base
# from database.setup import sync_engine
from schemas.districts import DistrictSchema
from services.service import Service
from utils.utils import get_logger
from errors import DateValidationError, ResultIsEmptyError
from utils.tasks import repeat_every
from utils.parser import parser
import uvicorn

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

    parser_logger.info("Выполняется задача по расписанию")

    service: Service = Service()

    districts_data: List[DistrictSchema] = []
    deadlines_data = get_deadlines_data()
    regions_data = get_regions_data()

    for district in get_districts_data():
        parser_logger.info(district)
        districts_data.append(DistrictSchema(**district))

    parser_logger.info(districts_data)
    flag, status = await service.districts.insert_districts(districts=districts_data)
    if flag:
        parser_logger.info("Вставка округов прошла успешно")
    else:
        parser_logger.critical(f"При вставке округов произошла ошибка {status}")
        parser_logger.critical("Выполнение задачи по расписанию оборвалось")
        return

    parser_logger.info("Выполнение задачи по расписанию завершено")


@app.exception_handler(DateValidationError)
async def date_validation_exception_handler(request: Request, e: DateValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": f"Invalid date format ({str(e).splitlines()[2].strip().split(' ')[2]}). Use YYYY-MM-DD."
        },
    )


@app.exception_handler(ResultIsEmptyError)
async def result_is_empty_exception_handler(request: Request, e: ResultIsEmptyError):
    return JSONResponse(status_code=400, content={"detail": str(e)})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
