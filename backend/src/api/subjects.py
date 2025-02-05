from typing import Annotated

from fastapi import APIRouter, Depends
from api.dependencies import subjects_service
from services.subjects import SubjectsService

router = APIRouter(
    prefix="/api/subjects",
    tags=["Subjects"],
)


@router.get("")
async def get_subjects(
     subjects_service: Annotated[SubjectsService, Depends(subjects_service)],
):
    subjects = await subjects_service.get_subjects()
    return subjects
