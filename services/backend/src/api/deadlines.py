from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import Response
from services.service import Service
from schemas.deadlines import DeadlinesSchema
from utils.utils import get_logger

logger = get_logger(logger_name="api.deadlines", file_name="backend")

router = APIRouter(
    prefix="/deadlines",
    tags=["Deadlines"],
)


@router.get("")
async def get_deadlines(
    service: Annotated[Service, Depends()],
) -> List[DeadlinesSchema]:

    deadlines = await service.deadlines.get_all_deadlines()
    return deadlines


@router.get("/{item_id}")
async def get_deadline_by_id(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
    service: Annotated[Service, Depends()],
) -> List[DeadlinesSchema]:

    deadlines = await service.deadlines.get_deadline_by_id(item_id)
    return deadlines


@router.post("")
async def insert_deadlines(
    service: Annotated[Service, Depends()],
    deadlines: List[DeadlinesSchema],
):

    flag, status = await service.deadlines.insert_deadlines(deadlines=deadlines)

    if flag:
        return Response(status_code=200)
    else:
        raise HTTPException(status_code=400)


@router.delete("/{item_id}")
async def delete_deadline(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
    service: Annotated[Service, Depends()],
):
    flag, status = await service.deadlines.delete_deadline_by_id(item_id)

    if flag:
        return Response(status_code=200)
    else:
        raise HTTPException(status_code=400)
