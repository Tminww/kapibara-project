from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, Request

from services import TableService as Service
from schemas import RequestTableSchema, ResponseSchema
from .dependencies import get_table_service as get_service
from utils import cache_response
from database import redis

router = APIRouter(prefix="/table", tags=["table"])


@router.get("")
async def get_table(
    params: RequestTableSchema,
    service: Annotated[Service, Depends(get_service)],
) -> ResponseSchema:
    print("HUI")
    print(params)
    response = await service.get_rows_from_table(params)
    print(response)
    return ResponseSchema(data=response)

