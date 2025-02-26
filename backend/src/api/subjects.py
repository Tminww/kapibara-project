from typing import Annotated

from fastapi import APIRouter, Depends
from api.dependencies import subjects_service
from services.statistics import StatisticsService

router = APIRouter(
    prefix="/api/subjects",
    tags=["Subjects"],
)


@router.get("")
async def get_subjects(
    subjects_service: Annotated[StatisticsService, Depends(subjects_service)],
):
    subjects = await subjects_service.get_subjects()

    return subjects
