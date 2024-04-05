from typing import Annotated
from repositories.statistics import StatisticsRepository
from repositories.subjects import SubjectsRepository
from repositories.regions import RegionsRepository

from services.statistics import StatisticsService
from services.subjects import SubjectsService
from services.regions import RegionsService


# def statistics_service():
#     return StatisticsService(StatisticsRepository)

# def subjects_service():
#     return SubjectsService(SubjectsRepository)


class Service:
    statistics = Annotated[StatisticsService, StatisticsService(StatisticsRepository)]
    subjects = Annotated[SubjectsService, SubjectsService(SubjectsRepository)]
    regions: RegionsService = RegionsService(RegionsRepository)
