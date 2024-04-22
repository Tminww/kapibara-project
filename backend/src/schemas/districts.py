from pydantic import BaseModel


class DistrictSchema(BaseModel):
    id: int
    name: str
    short_name: str
