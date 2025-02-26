from datetime import datetime
from typing import Annotated, Literal, Union, Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import ValidationError

from api.dependencies import statistics_service
from schemas.statistics import (
    DistrictsStatDTO,
    RequestBodySchema,
    RequestMaxMinBodySchema,
    ResponseStatDTO,
)
from services.statistics import StatisticsService
from errors import DateValidationError, ResultIsEmptyError

router = APIRouter(
    prefix="/api/statistics",
    tags=["Statistic in regions"],
)


def check_dates(start_date, end_date):
    current_date = datetime.now().strftime("%Y-%m-%d")

    if start_date is None and end_date is None:
        start_date = None
        end_date = None
    elif start_date is None and end_date is not None:
        start_date = end_date
        end_date = end_date
    elif start_date is not None and end_date is None:
        start_date = start_date
        end_date = current_date
    elif start_date is not None and end_date is not None:
        start_date = start_date
        end_date = end_date

    return start_date, end_date


@router.get("")
async def get_documents_in_districts(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    regions: Union[str, None] = None,
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
):
    try:
        startDate, endDate = check_dates(startDate, endDate)

        print(regions)
        print(startDate)
        print(endDate)

        if regions:
            regions = [int(region) for region in str(regions).split(",")]
            print(regions)

        parameters = RequestBodySchema(
            regions=regions, start_date=startDate, end_date=endDate
        )
        print(parameters)
    except ValueError as e:
        raise DateValidationError(e)
    else:
        documents = await statistics_service.get_stat_in_districts(parameters)
        documents.startDate = startDate if startDate is not None else None
        documents.endDate = endDate if endDate is not None else None
        return documents


@router.get("/subjects")
async def get_subjects_stat(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    regions: Union[str, None] = None,
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
):
    try:
        startDate, endDate = check_dates(startDate, endDate)

        print(regions)
        print(startDate)
        print(endDate)

        if regions:
            regions = [int(region) for region in str(regions).split(",")]
            print(regions)

        parameters = RequestBodySchema(
            regions=regions, start_date=startDate, end_date=endDate
        )
        print(parameters)
    except ValueError as e:
        raise DateValidationError(e)
    else:
        statistics = await statistics_service.get_subjects_stat(parameters)
        statistics.startDate = startDate if startDate is not None else None
        statistics.endDate = endDate if endDate is not None else None
        return statistics


@router.get("/districts")
async def get_districts_stat(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    regions: Union[str, None] = None,
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
):
    try:
        startDate, endDate = check_dates(startDate, endDate)

        print(regions)
        print(startDate)
        print(endDate)

        if regions:
            regions = [int(region) for region in str(regions).split(",")]
            print(regions)

        parameters = RequestBodySchema(
            regions=regions, start_date=startDate, end_date=endDate
        )
        print(parameters)
    except ValueError as e:
        raise DateValidationError(e)
    else:
        statistics = await statistics_service.get_districts_stat(parameters)
        startDate = startDate if startDate is not None else None
        endDate = endDate if endDate is not None else None
        return DistrictsStatDTO(
            name="Статистика за ФО",
            startDate=startDate,
            endDate=endDate,
            districts=statistics,
        )


@router.get("/publication-by-nomenclature")
async def get_publication_by_nomenclature(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
) -> ResponseStatDTO:
    try:
        startDate, endDate = check_dates(startDate, endDate)

        parameters = RequestBodySchema(start_date=startDate, end_date=endDate)
    except ValueError as e:
        raise DateValidationError(e)
    else:
        statistics = await statistics_service.get_publication_by_nomenclature(
            parameters
        )

        return statistics


@router.get("/publication-by-years")
async def get_publication_by_years(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    limit: int = 30,
) -> ResponseStatDTO:

    statistics = await statistics_service.get_publication_by_years(limit)

    return statistics


@router.get("/publication-by-districts")
async def get_publication_by_districts(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
) -> ResponseStatDTO:
    try:
        startDate, endDate = check_dates(startDate, endDate)

        parameters = RequestBodySchema(start_date=startDate, end_date=endDate)
    except ValueError as e:
        raise DateValidationError(e)
    else:
        statistics = await statistics_service.get_publication_by_districts(parameters)

        return statistics


@router.get("/publication-by-regions")
async def get_publication_by_regions(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
    limit: int = 10,
    sort: Literal["max", "min"] = "max",
) -> ResponseStatDTO:
    try:
        startDate, endDate = check_dates(startDate, endDate)

        parameters = RequestMaxMinBodySchema(
            start_date=startDate, end_date=endDate, limit=limit, sort=sort
        )
    except ValueError as e:
        raise DateValidationError(e)
    else:
        statistics = await statistics_service.get_publication_by_regions(parameters)

        return statistics


@router.get("/publication-by-nomenclature-detail")
async def get_publication_by_nomenclature_detail(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
) -> ResponseStatDTO:
    try:
        startDate, endDate = check_dates(startDate, endDate)

        parameters = RequestBodySchema(start_date=startDate, end_date=endDate)
    except ValueError as e:
        raise DateValidationError(e)
    else:
        statistics = await statistics_service.get_publication_by_nomenclature_detail(
            parameters
        )

        return statistics
