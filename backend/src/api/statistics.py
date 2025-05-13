from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request

from schemas import (
    RequestBodySchema,
    ResponseStatSchema,
)

from services import StatisticService as Service
from .dependencies import get_statistics_service as get_service
from utils import cache_response
from database import redis

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("")
@cache_response(backend=redis)
async def get_statistics(
    request: Request,
    service: Annotated[Service, Depends(get_service)],
    params: Annotated[RequestBodySchema, Query()],
) -> ResponseStatSchema:

    statistics = await service.get_stat_in_districts(params)
    return ResponseStatSchema(
        data=statistics,
        startDate=params.start_date,
        endDate=params.end_date,
    )


@router.get("/districts")
@cache_response(backend=redis)
async def get_districts_stat(
    request: Request,
    service: Annotated[Service, Depends(get_service)],
    params: Annotated[RequestBodySchema, Query()],
) -> ResponseStatSchema:

    statistics = await service.get_stat_districts(params)
    return ResponseStatSchema(
        data=statistics,
        startDate=params.start_date,
        endDate=params.end_date,
    )


@router.get("/districts/{dist_id}")
@cache_response(backend=redis)
async def get_districts_stat(
    request: Request,
    dist_id: int,
    params: Annotated[RequestBodySchema, Query()],
    service: Annotated[Service, Depends(get_service)],
) -> ResponseStatSchema:

    statistics = await service.get_stat_districts_by_id(dist_id, params)
    return ResponseStatSchema(
        data=statistics,
        startDate=params.start_date,
        endDate=params.end_date,
    )
