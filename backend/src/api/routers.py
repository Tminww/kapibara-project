from src.api.subjects import router as router_subjects
from src.api.statistics import router as router_statistics
from src.api.regions import router as router_regions
from src.api.districts import router as router_districts
from src.api.deadlines import router as router_deadlines
from src.api.dashboard import router as router_dashboard

all_routers = [
    router_subjects,
    router_statistics,
    router_regions,
    router_districts,
    router_deadlines,
    router_dashboard,
]
