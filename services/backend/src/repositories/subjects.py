from models.models import *
from utils.repository import SQLAlchemyRepository


class SubjectsRepository(SQLAlchemyRepository):
    district = DistrictEntity
    region = RegionEntity
