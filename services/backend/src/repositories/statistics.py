from models.document import DocumentEntity
from models.act import ActEntity
from models.region import RegionEntity
from models.models import DistrictEntity
from utils.repository import SQLAlchemyRepository


class StatisticsRepository(SQLAlchemyRepository):
    district = DistrictEntity
    document = DocumentEntity
    region = RegionEntity
    act = ActEntity
