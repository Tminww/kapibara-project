from src.models.documents import DocumentEntity
from src.models.regions import RegionEntity
from src.models.districts import DistrictEntity
from src.utils.repository import SQLAlchemyRepository


class SubjectsRepository(SQLAlchemyRepository):
    district = DistrictEntity
    region = RegionEntity
