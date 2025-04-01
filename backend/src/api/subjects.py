from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query

from services import SubjectService as Service
from schemas import RequestRegionSchema, ResponseSchema
from .dependencies import get_subjects_service as get_service

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.get("")
async def get_subjects(
    service: Annotated[Service, Depends(get_service)],
) -> ResponseSchema:
    subjects = await service.get_subjects()
    return ResponseSchema(data=subjects)


@router.get("/regions")
async def get_regions(
    params: Annotated[RequestRegionSchema, Query()],
    service: Annotated[Service, Depends(get_service)],
) -> ResponseSchema:
    regions = await service.get_regions(params)
    return ResponseSchema(data=regions)


@router.get("/districts")
async def get_districts(
    service: Annotated[Service, Depends(get_service)],
) -> ResponseSchema:
    districts = await service.get_districts()
    return ResponseSchema(data=districts)
