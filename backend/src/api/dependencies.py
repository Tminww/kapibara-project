from src.repositories import StatisticRepository, SubjectRepository, DashboardRepository

from src.services import StatisticService, DashboardService, SubjectService


def get_statistics_service():
    return StatisticService(StatisticRepository)


def get_subjects_service():
    return SubjectService(SubjectRepository)


def get_dashboard_service():
    return DashboardService(DashboardRepository)
