from pydantic import BaseModel, validator

class RegionInfoDTO(BaseModel):
    name: str
    id: int
    
    class Config:
        validate_assignment = True



class RegionsInDistrictDTO(BaseModel):
    name: str
    id: int
    regions: list[RegionInfoDTO]

    class Config:
        validate_assignment = True
