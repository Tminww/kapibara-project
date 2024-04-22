from models.documents import DocumentEntity
from models.regions import RegionEntity
from models.districts import DistrictEntity
from utils.repository import SQLAlchemyRepository


class SubjectsRepository(SQLAlchemyRepository):
    district = DistrictEntity
    region = RegionEntity
