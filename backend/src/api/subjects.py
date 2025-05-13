from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, Request

from services import SubjectService as Service
from schemas import RequestRegionSchema, ResponseSchema
from .dependencies import get_subjects_service as get_service
from utils import cache_response
from database import redis

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.get("")
@cache_response(backend=redis)
async def get_subjects(
    request: Request,
    service: Annotated[Service, Depends(get_service)],
) -> ResponseSchema:
    subjects = await service.get_subjects()
    return ResponseSchema(data=subjects)


@router.get("/regions")
@cache_response(backend=redis)
async def get_regions(
    request: Request,
    params: Annotated[RequestRegionSchema, Query()],
    service: Annotated[Service, Depends(get_service)],
) -> ResponseSchema:
    regions = await service.get_regions(params)
    return ResponseSchema(data=regions)


@router.get("/districts")
@cache_response(backend=redis)
async def get_districts(
    request: Request,
    service: Annotated[Service, Depends(get_service)],
) -> ResponseSchema:
    districts = await service.get_districts()
    return ResponseSchema(data=districts)
