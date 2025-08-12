from repositories import (StatisticRepository, SubjectRepository, DashboardRepository, TableRepository)

from services import (StatisticService, DashboardService, SubjectService, TableService)


def get_statistics_service():
    return StatisticService(StatisticRepository)


def get_subjects_service():
    return SubjectService(SubjectRepository)


def get_dashboard_service():
    return DashboardService(DashboardRepository)

def get_table_service():
    return TableService(TableRepository)