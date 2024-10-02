from typing import Annotated, Union, Optional, List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

# from api.dependencies import statistics_service
from src.services.service import Service
from src.schemas.statistics import RequestBodySchema
from src.services.statistics import StatisticsService
from src.errors import DateValidationError, ResultIsEmptyError

router = APIRouter(
    prefix="/dashboard",
    tags=["Statistics"],
)


@router.get("/districts/{district_id}/regions/{region_id}")
async def get_documents_in_districts(
    service: Annotated[Service, Depends()],
    district_id: int,
    region_id: int,
    startDate: Union[str, None] = None,
    endDate: Union[str, None] = None,
):
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": {"district_id": district_id, "region_id": region_id, "startDate": startDate, "endDate": endDate}})
    # try:
        
    #     parameters = RequestBodySchema(
    #         regions=regions, start_date=startDate, end_date=endDate
    #     )
    #     print(parameters)
    # except ValueError as e:
    #     raise DateValidationError(e)
    # else:
    #     documents = await service.statistics.get_stat_in_districts(parameters)
    #     return documents
