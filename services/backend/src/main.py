from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from api.routers import all_routers

# from models.base import Base
# from database.setup import sync_engine
from utils import utils
from errors import DateValidationError, ResultIsEmptyError
from utils.tasks import repeat_every
import uvicorn

logger = utils.get_logger("fastapi.main")


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
    
logger = utils.get_logger("task")

@app.on_event("startup")
@repeat_every(seconds=5, logger=logger)
async def test_task():
    logger.info("Выполняется задача по расписанию")

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