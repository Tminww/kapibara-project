from .base import BaseSchema


class RegionSchema(BaseSchema):
    id: int
    name: str
    short_name: str
    external_id: str
    code: str
    parent_id: str
    id_dist: int


class RegionInfoSchema(BaseSchema):
    id: int
    name: str
