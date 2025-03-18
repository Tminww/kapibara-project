from pydantic import BaseModel


class RegionSchema(BaseModel):
    id: int
    name: str
    short_name: str
    external_id: str
    code: str
    parent_id: str
    id_dist: int
