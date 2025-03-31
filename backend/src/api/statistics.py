from typing import Annotated
from fastapi import APIRouter, Depends, Query

from src.schemas import (
    RequestBodySchema,
    ResponseStatSchema,
)

from src.services import StatisticService as Service
from .dependencies import get_statistics_service as get_service

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("")
async def get_statistics(
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
async def get_districts_stat(
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
async def get_districts_stat(
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
