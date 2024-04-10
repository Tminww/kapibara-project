from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from services.service import Service
from schemas.districts import DistrictSchema
from utils.utils import get_logger

logger = get_logger(logger_name="api.districts", file_name="backend")

router = APIRouter(
    prefix="/districts",
    tags=["Districts"],
)


@router.get("")
async def get_districts(
    service: Annotated[Service, Depends()],
) -> List[DistrictSchema]:
    logger.info("get_districts")
    districts = await service.districts.get_all_districts()
    return districts


@router.post("")
async def insert_districts(
    service: Annotated[Service, Depends()],
    districts: List[DistrictSchema],
):
    logger.info("insert_districts")

    flag, status = await service.districts.insert_districts(districts=districts)

    if flag:
        return Response(status_code=200)
    else:
        raise HTTPException(status_code=400)
