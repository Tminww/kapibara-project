from typing import Annotated, Literal, Union, Optional, List
from fastapi import APIRouter, Depends, Query

from schemas import (
    RequestBodySchema,
    RequestMaxMinBodySchema,
    ResponseStatSchema,
    RequestSchema,
    RequestNomenclatureSchema,
)
from services import DashboardService as Service
from .dependencies import get_dashboard_service as get_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


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


@router.get("/nomenclature")
async def get_publication_by_nomenclature(
    service: Annotated[Service, Depends(get_service)],
    params: Annotated[RequestNomenclatureSchema, Query()],
) -> ResponseStatSchema:

    if params.detail:
        statistics = await service.get_publication_by_nomenclature_detail(params)
    else:
        statistics = await service.get_publication_by_nomenclature(params)

    return ResponseStatSchema(
        data=statistics,
        startDate=params.start_date,
        endDate=params.end_date,
    )


@router.get("/years")
async def get_publication_by_years(
    service: Annotated[Service, Depends(get_service)],
    limit: int = Query(default=30, ge=1, le=50),
) -> ResponseStatSchema:

    statistics = await service.get_publication_by_years(limit)

    return ResponseStatSchema(
        data=statistics,
        startDate=None,
        endDate=None,
    )


@router.get("/districts")
async def get_publication_by_districts(
    service: Annotated[Service, Depends(get_service)],
    params: Annotated[RequestSchema, Query()],
) -> ResponseStatSchema:

    statistics = await service.get_publication_by_districts(params)

    return ResponseStatSchema(
        data=statistics,
        startDate=params.start_date,
        endDate=params.end_date,
    )


@router.get("/regions")
async def get_publication_by_regions(
    service: Annotated[Service, Depends(get_service)],
    params: Annotated[RequestMaxMinBodySchema, Query()],
) -> ResponseStatSchema:

    statistics = await service.get_publication_by_regions(params)
    return ResponseStatSchema(
        data=statistics,
        startDate=params.start_date,
        endDate=params.end_date,
    )


@router.get("/types")
async def get_publication_by_types(
    service: Annotated[Service, Depends(get_service)],
    params: Annotated[RequestSchema, Query()],
) -> ResponseStatSchema:

    statistics = await service.get_publication_by_types(params)

    return ResponseStatSchema(
        data=statistics,
        startDate=None,
        endDate=params.end_date,
    )
