from typing import Union
from src.schemas.base import BaseSchema


class OrganInBlockSchema(BaseSchema):
    id: Union[int, None]
    name: str
    code: Union[str, None]
    external_id: str


class RegionInBlockSchema(BaseSchema):
    id: Union[int, None]
    name: str
    code: Union[str, None]
    external_id: str


class BlockSchema(BaseSchema):
    id: Union[int, None]
    organ: OrganInBlockSchema
    region: RegionInBlockSchema | None
