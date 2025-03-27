from repositories.statistics import StatisticsRepository
from services.statistics import StatisticsService

from repositories.subjects import SubjectsRepository
from services.subjects import SubjectsService


def get_statistics_service():
    return StatisticsService(StatisticsRepository)


def get_subjects_service():
    return SubjectsService(SubjectsRepository)
