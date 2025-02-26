from datetime import date, datetime
from pydantic import BaseModel, validator
from typing import Literal, Optional
from errors import DateValidationError

class ActSchema(BaseModel):
    id_act: int
    name: str
    npaId: str

    class Config:
        # from_attributes = True
        validate_assignment = True


class DocumentSchema(BaseModel):
    id_doc: int
    id_act: int
    complexName: str
    eoNumber: int
    viewDate: date
    pagesCount: int
    id_reg: int

    class Config:
        from_attributes = True
        validate_assignment = True


class StatRegionSchema(BaseModel):
    region_name: str
    count: int
    stat: Optional[list] = None

    class Config:
        from_attributes = True
        validate_assignment = True


class StatRegionsSchema(BaseModel):
    count: int
    regions: Optional[list[StatRegionSchema]] = None

    class Config:
        from_attributes = True
        validate_assignment = True


class StatRowSchema(BaseModel):
    region_name: str
    act_name: str
    count: int

    class Config:
        from_attributes = True
        validate_assignment = True


# создать дто для возвращения на сайт


class StatBaseDTO(BaseModel):
    name: Optional[str] = None
    count: Optional[int] = None

    class Config:
        from_attributes = True
        validate_assignment = True


class StatRegionDTO(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None
    count: Optional[int] = None
    stat: Optional[list[StatBaseDTO]] = None

    class Config:
        from_attributes = True
        validate_assignment = True


class SubjectsStatDTO(BaseModel):
    name: Optional[str] = None
    count: Optional[int] = None
    stat: Optional[list[StatBaseDTO]] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None

class ResponseStatDTO(BaseModel):
    name: Optional[str] = None
    count: Optional[int] = None
    stat: Optional[list[StatBaseDTO]] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None


class DistrictStatDTO(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None
    count: Optional[int] = None
    stat: Optional[list[StatBaseDTO]] = None
    
class DistrictsStatDTO(BaseModel):
    name: Optional[str] = None
    districts: Optional[list[DistrictStatDTO]] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None


class StatDistrictDTO(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None
    count: Optional[int] = None
    stat: Optional[list[StatBaseDTO]] = None
    regions: Optional[list[StatRegionDTO]] = None

    class Config:
        from_attributes = True
        validate_assignment = True


class StatAllDTO(BaseModel):
    name: Optional[str] = None
    count: Optional[int] = None
    stat: Optional[list[StatBaseDTO]] = None
    districts: Optional[list[StatDistrictDTO]] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None

    

    class Config:
        from_attributes = True
        validate_assignment = True



class RequestBodySchema(BaseModel):
    regions: Optional[list[int]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    @validator("start_date")
    def start_date_validator(cls, value):
        if value is not None:
            try:
                datetime.strptime(value, "%Y-%m-%d")
                return value
            except ValueError:
                print(value)
                raise ValueError(value)
        else:
            return value

    @validator("end_date")
    def end_date_validator(cls, value):
        if value is not None:
            try:
                datetime.strptime(value, "%Y-%m-%d")
                return value
            except ValueError:
                print(value)
                raise ValueError(value)
        else:
            return value

    class Config:
        # from_attributes = True
        validate_assignment = True
        
class RequestMaxMinBodySchema(RequestBodySchema):
    limit: Optional[int] = None
    sort: Literal['max', 'min'] = 'max'