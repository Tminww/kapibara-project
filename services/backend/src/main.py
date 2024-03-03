from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from api.routers import all_routers

from database.setup import init_db
from models import models
from errors import DateValidationError, ResultIsEmptyError

import uvicorn

app = FastAPI(title="Вывод статистики по документам")


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

# FIXME dev server for poetry
server = uvicorn.run(app=app, host="127.0.0.1", port=8000, log_level="info")


# metadata.create_all не выполняется асинхронно,
# поэтому мы использовали run_sync для его синхронного выполнения в асинхронной функции.
@app.on_event("startup")
async def on_startup():
    await init_db()


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
