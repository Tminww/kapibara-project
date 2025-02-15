from datetime import datetime
from typing import Annotated, Union, Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import ValidationError

from api.dependencies import statistics_service
from schemas.statistics import RequestBodySchema
from services.statistics import StatisticsService
from errors import DateValidationError, ResultIsEmptyError

router = APIRouter(
    prefix="/api/statistics",
    tags=["Statistic in regions"],
)


@router.get("")
async def get_documents_in_districts(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    regions: Union[str, None] = None,
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
):
    try:
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_date = datetime.strptime(current_date, "%Y-%m-%d")

        if startDate is None and endDate is None:
            startDate = None
            endDate = None
        elif startDate is None and endDate is not None:
            startDate = datetime.strptime(endDate, "%Y-%m-%d")
            endDate = datetime.strptime(endDate, "%Y-%m-%d")
        elif startDate is not None and endDate is None:
            startDate = datetime.strptime(startDate, "%Y-%m-%d")
            endDate = current_date
        elif startDate is not None and endDate is not None:
            startDate = datetime.strptime(startDate, "%Y-%m-%d")
            endDate = datetime.strptime(endDate, "%Y-%m-%d")
        
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
        return documents
