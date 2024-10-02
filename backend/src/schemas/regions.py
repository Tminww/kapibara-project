from typing import Optional
from src.schemas.base import BaseSchema


class MockRegionSchema(BaseSchema):
    id_dist: int
    name: str


class PravoGovRegionSchema(BaseSchema):

    name: str
    short_name: str
    external_id: str
    code: str
    parent_id: Optional[str]


class RegionSchema(PravoGovRegionSchema):
    id: int | None
    id_dist: Optional[int]
