from typing import Optional
from pydantic import BaseModel


class MockRegionSchema(BaseModel):
    id_dist: int
    name: str


class PravoGovRegionSchema(BaseModel):
    name: str
    short_name: str
    external_id: str
    code: str
    parent_id: Optional[str]


class RegionSchema(PravoGovRegionSchema):
    id_dist: Optional[int]
