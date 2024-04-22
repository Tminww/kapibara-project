from src.api.subjects import router as router_subjects
from src.api.statistics import router as router_statistics
from src.api.regions import router as router_regions
from src.api.districts import router as router_districts
from src.api.deadlines import router as router_deadlines

all_routers = [
    router_subjects,
    router_statistics,
    router_regions,
    router_districts,
    router_deadlines,
]
