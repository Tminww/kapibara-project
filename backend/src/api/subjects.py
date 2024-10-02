from typing import Annotated

from fastapi import APIRouter, Depends

from src.services.service import Service

from src.utils import utils

logger = utils.get_logger("fastapi.api.subjects")

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"],
)


@router.get("")
async def get_subjects(
    service: Annotated[Service, Depends()],
):
    logger.info("get_subjects")
    subjects = await service.subjects.get_subjects()
    return subjects
