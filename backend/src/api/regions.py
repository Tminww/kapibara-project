from typing import Annotated, List

from fastapi import APIRouter, Depends
from schemas.regions import PravoGovRegionSchema
from services.service import Service

from utils.utils import get_logger

logger = get_logger("api.regions")

router = APIRouter(
    prefix="/regions",
    tags=["Regions"],
)


@router.get("")
async def get_regions(
    service: Annotated[Service, Depends()],
) -> List[PravoGovRegionSchema]:
    logger.info("get_regions")
    regions = await service.regions.get_all_regions()
    return regions
