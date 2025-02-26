from repositories.statistics import SQLAlchemyRepository

from services.statistics import StatisticsService


def statistics_service():
    return StatisticsService(SQLAlchemyRepository)
