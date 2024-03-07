from models.documents import *
from utils.repository import SQLAlchemyRepository


class SubjectsRepository(SQLAlchemyRepository):
    district = DistrictEntity
    region = RegionEntity
