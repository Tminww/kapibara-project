from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .api import routers
from .errors import (
    DataDelitionError,
    DataInsertionError,
    DateValidationError,
    ResultIsEmptyError,
)
from .parser.main import parse
from .utils import backend_logger as logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before app starts
    # await parse()
    yield
    # After app ends


app = FastAPI(title="Вывод статистики по документам", lifespan=lifespan)


# настройка CORS
origins = [
    "http://localhost:5173",
]

# настройка middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# настройка роутеров
for router in routers:
    app.include_router(router, prefix="/api")


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
