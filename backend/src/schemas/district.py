from pydantic import BaseModel
from .region import RegionSchema


class DistrictSchema(BaseModel):
    name: str
    id: int
    short_name: str


class DistrictWithRegionsSchema(DistrictSchema):
    regions: list[RegionSchema]
