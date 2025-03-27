from datetime import datetime
from typing import Annotated, Literal, Union, Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import ValidationError

from api.dependencies import statistics_service
from schemas import (
    RequestBodySchema,
    RequestMaxMinBodySchema,
    ResponseStatSchema,
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
            ids=regions, start_date=startDate, end_date=endDate
        )
        print(parameters)
    except ValueError as e:
        raise DateValidationError(e)
    else:
        documents = await statistics_service.get_stat_in_districts(parameters)

        return ResponseStatSchema(
            data=documents,
            startDate=startDate if startDate is not None else None,
            endDate=endDate if endDate is not None else None,
        )


@router.get("/subjects")
async def get_subjects_stat(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    regions: Union[str, None] = None,
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
):
    try:
        startDate, endDate = check_dates(startDate, endDate)

        if regions:
            regions = [int(region) for region in str(regions).split(",")]

        parameters = RequestBodySchema(
            ids=regions, start_date=startDate, end_date=endDate
        )
        print(parameters)
    except ValueError as e:
        raise DateValidationError(e)
    else:
        statistics = await statistics_service.get_subjects_stat(parameters)

        return ResponseStatSchema(
            data=statistics,
            startDate=startDate if startDate is not None else None,
            endDate=endDate if endDate is not None else None,
        )


@router.get("/districts")
async def get_districts_stat(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    districts: Union[str, None] = None,
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
):
    try:
        startDate, endDate = check_dates(startDate, endDate)

        print(districts)
        print(startDate)
        print(endDate)

        if districts:
            districts = [int(region) for region in str(districts).split(",")]
            print(districts)

        parameters = RequestBodySchema(
            ids=districts, start_date=startDate, end_date=endDate
        )
        print(parameters)
    except ValueError as e:
        raise DateValidationError(e)
    else:
        statistics = await statistics_service.get_districts_stat(parameters)

        return ResponseStatSchema(
            data=statistics,
            startDate=startDate if startDate is not None else None,
            endDate=endDate if endDate is not None else None,
        )


@router.get("/publication-by-nomenclature")
async def get_publication_by_nomenclature(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
) -> ResponseStatSchema:
    try:
        startDate, endDate = check_dates(startDate, endDate)

        parameters = RequestBodySchema(start_date=startDate, end_date=endDate)
    except ValueError as e:
        raise DateValidationError(e)
    else:
        statistics = await statistics_service.get_publication_by_nomenclature(
            parameters
        )

        return ResponseStatSchema(
            data=statistics,
            startDate=startDate if startDate is not None else None,
            endDate=endDate if endDate is not None else None,
        )


@router.get("/publication-by-years")
async def get_publication_by_years(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    limit: int = 30,
) -> ResponseStatSchema:

    statistics = await statistics_service.get_publication_by_years(limit)

    return ResponseStatSchema(
            data=statistics,
            startDate=None,
            endDate=None,
        )


@router.get("/publication-by-districts")
async def get_publication_by_districts(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
) -> ResponseStatSchema:
    try:
        startDate, endDate = check_dates(startDate, endDate)

        parameters = RequestBodySchema(start_date=startDate, end_date=endDate)
    except ValueError as e:
        raise DateValidationError(e)
    else:
        statistics = await statistics_service.get_publication_by_districts(parameters)

        return ResponseStatSchema(
            data=statistics,
            startDate=startDate if startDate is not None else None,
            endDate=endDate if endDate is not None else None,
        )


@router.get("/publication-by-regions")
async def get_publication_by_regions(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
    limit: int = 10,
    sort: Literal["max", "min"] = "max",
) -> ResponseStatSchema:
    try:
        startDate, endDate = check_dates(startDate, endDate)

        parameters = RequestMaxMinBodySchema(
            start_date=startDate, end_date=endDate, limit=limit, sort=sort
        )
    except ValueError as e:
        raise DateValidationError(e)
    else:
        statistics = await statistics_service.get_publication_by_regions(parameters)

        return ResponseStatSchema(
            data=statistics,
            startDate=startDate if startDate is not None else None,
            endDate=endDate if endDate is not None else None,
        )


@router.get("/publication-by-nomenclature-detail")
async def get_publication_by_nomenclature_detail(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
) -> ResponseStatSchema:
    try:
        startDate, endDate = check_dates(startDate, endDate)

        parameters = RequestBodySchema(start_date=startDate, end_date=endDate)
    except ValueError as e:
        raise DateValidationError(e)
    else:
        statistics = await statistics_service.get_publication_by_nomenclature_detail(
            parameters
        )

        return ResponseStatSchema(
            data=statistics,
            startDate=startDate if startDate is not None else None,
            endDate=endDate if endDate is not None else None,
        )


@router.get("/publication-by-acts")
async def get_publication_by_acts(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
) -> ResponseStatSchema:
    try:
        startDate, endDate = check_dates(startDate, endDate)

        parameters = RequestBodySchema(start_date=startDate, end_date=endDate)
    except ValueError as e:
        raise DateValidationError(e)
    else:
        statistics = await statistics_service.get_publication_by_acts(parameters)

        return ResponseStatSchema(
            data=statistics,
            startDate=startDate if startDate is not None else None,
            endDate=endDate if endDate is not None else None,
        )
