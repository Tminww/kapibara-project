from models.district import DistrictEntity
from models.region import RegionEntity
from utils.repository import SQLAlchemyRepository


class SubjectsRepository(SQLAlchemyRepository):
    district = DistrictEntity 
    region = RegionEntity
    