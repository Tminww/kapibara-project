from typing import Annotated, Literal, Union, Optional, List
from fastapi import APIRouter, Depends

from schemas import (
    RequestBodySchema,
    RequestMaxMinBodySchema,
    ResponseStatSchema,
    RequestSchema,
)

from services.statistics import StatisticsService as Service
from .dependencies import get_statistics_service as get_service
from errors import DateValidationError

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("")
async def get_statistics(
    service: Annotated[Service, Depends(get_service)],
    params: RequestBodySchema,
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
    params: RequestBodySchema,
) -> ResponseStatSchema:

    statistics = await service.get_districts_stat(params)
    return ResponseStatSchema(
        data=statistics,
        startDate=params.start_date,
        endDate=params.end_date,
    )
