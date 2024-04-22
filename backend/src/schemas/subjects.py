from pydantic import BaseModel, validator

class SubjectInfoDTO(BaseModel):
    name: str
    id: int



class SubjectsInDistrictDTO(BaseModel):
    name: str
    id: int
    regions: list[SubjectInfoDTO]
