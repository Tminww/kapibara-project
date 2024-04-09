from datetime import date, datetime
from pydantic import BaseModel, validator
from typing import Optional
from errors import DateValidationError


class DistrictSchema(BaseModel):
    id: int
    name: str
    short_name: str
