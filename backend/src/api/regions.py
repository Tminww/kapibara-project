from typing import Annotated, List
from fastapi import APIRouter, Depends

from src.schemas.regions import RegionDTO
from src.services.service import Service
from src.utils.utils import get_logger

logger = get_logger("api.regions")

router = APIRouter(
    prefix="/regions",
    tags=["Regions"],
)


@router.get("")
async def get_regions(
    service: Annotated[Service, Depends()],
) -> List[RegionDTO]:
    logger.info("get_regions")
    regions = await service.regions.get_all_regions()

    print(regions)
    return regions
