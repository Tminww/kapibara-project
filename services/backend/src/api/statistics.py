from typing import Annotated, Union, Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import ValidationError

from api.dependencies import statistics_service
from schemas.statistics import RequestBodySchema
from services.statistics import StatisticsService
from errors import DateValidationError, ResultIsEmptyError

router = APIRouter(
    prefix="/statistics",
    tags=["Statistic in regions"],
)


@router.get("")
async def get_documents_in_districts(
    statistics_service: Annotated[StatisticsService, Depends(statistics_service)],
    regions: Union[List[int], None] = Query(None),
    start_date: Union[str, None] = None,
    end_date: Union[str, None] = None,
):
    try:
        parameters = RequestBodySchema(
            regions=regions, start_date=start_date, end_date=end_date
        )
        # return(parameters)
    except ValueError as e:
        raise DateValidationError(e)
    else:
        documents = await statistics_service.get_stat_in_districts(parameters)
        return documents
