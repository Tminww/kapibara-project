from typing import Annotated, Union, Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import ValidationError

# from api.dependencies import statistics_service
from services.service import Service
from schemas.statistics import RequestBodySchema
from services.statistics import StatisticsService
from errors import DateValidationError, ResultIsEmptyError

router = APIRouter(
    prefix="/statistics",
    tags=["Statistic in regions"],
)


@router.get("")
async def get_documents_in_districts(
    service: Annotated[Service, Depends()],
    regions: Union[str, None] = None,
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
):
    try:
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
        documents = await service.statistics.get_stat_in_districts(parameters)
        return documents
