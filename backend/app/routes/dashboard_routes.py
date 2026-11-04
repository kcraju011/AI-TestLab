from fastapi import APIRouter

from app.dashboard.dashboard_service import DashboardService
from app.models.dashboard_schemas import DashboardSummary


router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)

dashboard_service = DashboardService()


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary():
    return dashboard_service.get_summary()