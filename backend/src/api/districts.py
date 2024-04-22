from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import Response
from src.services.service import Service
from src.schemas.districts import DistrictSchema
from src.utils.utils import get_logger

logger = get_logger(logger_name="api.districts", file_name="backend")

router = APIRouter(
    prefix="/districts",
    tags=["Districts"],
)


@router.get("", description="Get all districts")
async def get_districts(
    service: Annotated[Service, Depends()],
) -> List[DistrictSchema]:

    districts = await service.districts.get_all_districts()
    return districts


@router.get("/{item_id}", description="Get district by ID")
async def get_district_by_id(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
    service: Annotated[Service, Depends()],
) -> List[DistrictSchema]:

    districts = await service.districts.get_district_by_id(item_id)
    return districts


@router.post("", description="Insert or Update districts")
async def insert_districts(
    service: Annotated[Service, Depends()],
    districts: List[DistrictSchema],
):

    flag, status = await service.districts.insert_districts(districts=districts)

    if flag:
        return Response(status_code=200)
    else:
        raise HTTPException(status_code=400)
