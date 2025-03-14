from src.schemas.base import BaseSchema


class DistrictDTO(BaseSchema):
    id: int
    name: str
    short_name: str
