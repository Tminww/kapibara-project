from repositories.statistics import StatisticsRepository
from repositories.subjects import SubjectsRepository

from services.statistics import StatisticsService
from services.subjects import SubjectsService


def statistics_service():
    return StatisticsService(StatisticsRepository)

def subjects_service():
    return SubjectsService(SubjectsRepository)


