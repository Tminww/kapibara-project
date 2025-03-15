from typing import Any
from .base import BaseSchema


class ResponseSchema(BaseSchema):
    data: Any


class ResponseStatSchema(ResponseSchema):
    startDate: str = None
    endDate: str = None
