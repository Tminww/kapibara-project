from typing import Optional
from .base import BaseSchema


class StatBaseSchema(BaseSchema):
    name: str = None
    count: int = None


class StatRegionSchema(BaseSchema):
    name: str = None
    id: int = None
    count: int = None
    stat: Optional[list[StatBaseSchema]] = None


class StatDistrictSchema(BaseSchema):
    name: str = None
    id: int = None
    count: int = None
    stat: list[StatBaseSchema] = None
    regions: Optional[list[StatRegionSchema]] = None


class StatAllSchema(BaseSchema):
    name: str = None
    count: int = None
    stat: list[StatBaseSchema] = None
    districts: Optional[list[StatDistrictSchema]] = None

class StatPublicationSchema(BaseSchema):
    name: str = None
    count: int = None
    stat: list[StatBaseSchema] = None
