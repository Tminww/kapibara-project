from src.schemas.base import BaseSchema


class DistrictSchema(BaseSchema):
    id: int
    name: str
    short_name: str
