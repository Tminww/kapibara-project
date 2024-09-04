from src.schemas.base import BaseSchema


class OrganInBlockSchema(BaseSchema):
    id: int | None
    name: str
    code: str | None
    external_id: str


class RegionInBlockSchema(BaseSchema):
    id: int | None
    name: str
    code: str | None
    external_id: str


class BlockSchema(BaseSchema):
    id: int | None
    organ: OrganInBlockSchema
    region: RegionInBlockSchema | None
