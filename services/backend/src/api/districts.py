from typing import Annotated

from fastapi import APIRouter, Depends
from services.service import Service

from utils.utils import get_logger

logger = get_logger("api.districts")

router = APIRouter(
    prefix="/districts",
    tags=["Districts"],
)


@router.get("")
async def get_districts(
    service: Annotated[Service, Depends()],
):
    logger.info("get_districts")
    districts = await service.districts.get_all_districts()
    return districts
