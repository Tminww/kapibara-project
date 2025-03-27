from typing import Annotated, Optional

from fastapi import APIRouter, Depends

from services.subjects import SubjectsService as Service
from schemas import RequestRegionSchema
from .dependencies import get_subjects_service as get_service

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.get("")
async def get_subjects(
    service: Annotated[Service, Depends(get_service)],
):
    subjects = await service.get_subjects()
    return subjects


@router.get("/regions")
async def get_regions(
    service: Annotated[Service, Depends(get_service)],
    params: RequestRegionSchema,
):
    if params.districtName and params.districtName:
        raise ValueError("districtName or districtId must be provided")
    regions = await service.get_regions(params)
    return regions


@router.get("/districts")
async def get_districts(
    service: Annotated[Service, Depends(get_service)],
):
    districts = await service.get_districts()
    return districts
