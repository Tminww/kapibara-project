from typing import Annotated

from fastapi import APIRouter, Depends
from api.dependencies import subjects_service
from services.subjects import SubjectsService

from utils import utils

logger = utils.get_logger("fastapi.api.subjects")

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"],
)


@router.get("")
async def get_subjects(
    subjects_service: Annotated[SubjectsService, Depends(subjects_service)],
):
    logger.info("get_subjects")
    subjects = await subjects_service.get_subjects()
    return subjects
