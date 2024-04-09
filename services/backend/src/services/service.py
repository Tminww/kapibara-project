from typing import Annotated
from repositories.statistics import StatisticsRepository
from repositories.subjects import SubjectsRepository
from repositories.regions import RegionsRepository
from repositories.districts import DistrictsRepository

from services.statistics import StatisticsService
from services.subjects import SubjectsService
from services.regions import RegionsService
from services.districts import DistrictsService


# def statistics_service():
#     return StatisticsService(StatisticsRepository)

# def subjects_service():
#     return SubjectsService(SubjectsRepository)


class Service:
    statistics: StatisticsService = StatisticsService(StatisticsRepository)
    subjects: SubjectsService = SubjectsService(SubjectsRepository)
    regions: RegionsService = RegionsService(RegionsRepository)
    districts: DistrictsService = DistrictsService(DistrictsRepository)
