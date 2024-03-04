from models.models import *

from utils.repository import SQLAlchemyRepository


class StatisticsRepository(SQLAlchemyRepository):
    district = DistrictEntity
    document = DocumentEntity
    region = RegionEntity
    # act = ActEntity
