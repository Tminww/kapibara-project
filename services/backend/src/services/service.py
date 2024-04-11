from typing import Annotated
from repositories.statistics import StatisticsRepository
from repositories.subjects import SubjectsRepository
from repositories.regions import RegionsRepository
from repositories.districts import DistrictsRepository
from repositories.deadlines import DeadlinesRepository

from services.statistics import StatisticsService
from services.subjects import SubjectsService
from services.regions import RegionsService
from services.districts import DistrictsService
from services.deadlines import DeadlinesService


class Service:
    statistics: StatisticsService = StatisticsService(StatisticsRepository)
    subjects: SubjectsService = SubjectsService(SubjectsRepository)
    regions: RegionsService = RegionsService(RegionsRepository)
    districts: DistrictsService = DistrictsService(DistrictsRepository)
    deadlines: DeadlinesService = DeadlinesService(DeadlinesRepository)
