from typing import Any, Optional
from .base import BaseSchema


class ResponseSchema(BaseSchema):
    data: Any


class ResponseStatSchema(ResponseSchema):
    startDate: Optional[str] = None
    endDate: Optional[str] = None
