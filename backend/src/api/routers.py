from .subjects import router as router_subjects
from .statistics import router as router_statistics
from .dashboard import router as router_dashboard

routers = [router_subjects, router_statistics, router_dashboard]
