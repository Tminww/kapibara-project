from typing import Annotated, List


from fastapi import APIRouter, Depends, Path
from fastapi import status
from fastapi.responses import JSONResponse, Response
from services.service import Service
from schemas.deadlines import DeadlinesSchema
from utils.utils import get_logger
from errors import DataDelitionError, DataInsertionError

logger = get_logger(logger_name="api.deadlines", file_name="backend")

router = APIRouter(
    prefix="/deadlines",
    tags=["Deadlines"],
)


@router.get("")
async def get_deadlines(
    service: Annotated[Service, Depends()],
) -> List[DeadlinesSchema]:
    """
    Retrieve all deadlines from the database.
    """
    deadlines = await service.deadlines.get_all_deadlines()
    return deadlines


@router.get("/{item_id}")
async def get_deadline_by_id(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
    service: Annotated[Service, Depends()],
) -> List[DeadlinesSchema]:
    """
    Retrieve a specific deadline by its ID from the database.
    """
    deadlines = await service.deadlines.get_deadline_by_id(item_id)
    return deadlines


@router.post("")
async def insert_deadlines(
    service: Annotated[Service, Depends()],
    deadlines: List[DeadlinesSchema],
):
    """
    Insert a list of deadlines into the database.
    """
    flag, error = await service.deadlines.insert_deadlines(deadlines=deadlines)

    if flag:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"detail": "Insert a list of deadlines is successful"},
        )
    else:

        raise DataInsertionError(error)


@router.delete("/{item_id}")
async def delete_deadline(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
    service: Annotated[Service, Depends()],
):
    """
    Delete a specific deadline by its ID from the database.
    """

    try:
        flag, error = await service.deadlines.delete_deadline_by_id(item_id)
        if flag:
            return JSONResponse(
                status_code=status.HTTP_205_RESET_CONTENT,
                content={"detail": "Deadline successfully deleted"},
            )
    except Exception as e:
        raise DataDelitionError(f"An error occurred while deleting: {e}")
