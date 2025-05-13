from .base import BaseSchema
from .region import RegionSchema


class DistrictSchema(BaseSchema):
    name: str
    id: int
    short_name: str


class DistrictWithRegionsSchema(DistrictSchema):
    regions: list[RegionSchema]
