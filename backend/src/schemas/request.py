from datetime import datetime
from typing import Literal, Optional
from pydantic import validator
from .base import BaseSchema


class RequestBodySchema(BaseSchema):
    ids: Optional[list[int]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    @validator("start_date")
    def start_date_validator(cls, value):
        if value is not None:
            try:
                datetime.strptime(value, "%Y-%m-%d")
                return value
            except ValueError:
                print(value)
                raise ValueError(value)
        else:
            return value

    @validator("end_date")
    def end_date_validator(cls, value):
        if value is not None:
            try:
                datetime.strptime(value, "%Y-%m-%d")
                return value
            except ValueError:
                print(value)
                raise ValueError(value)
        else:
            return value


class RequestMaxMinBodySchema(RequestBodySchema):
    limit: int = None
    sort: Literal["max", "min"] = "max"
