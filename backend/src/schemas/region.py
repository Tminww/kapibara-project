from pydantic import BaseModel


class RegionSchema(BaseModel):
    id: int
    name: str
    short_name: str
    code: str
