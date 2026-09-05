"""Analytics and dashboard API routes."""

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import PlainTextResponse

from app.api.deps import CurrentUser, DbSession
from app.repositories.machine_repository import MachineRepository
from app.repositories.sensor_reading_repository import SensorReadingRepository
from app.repositories.alert_repository import AlertRepository
from app.repositories.maintenance_repository import MaintenanceRepository
from app.schemas import AnalyticsSummary, DashboardStats, MachineTrends, SensorReadingResponse, AlertResponse, MaintenanceResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(db: DbSession, _: CurrentUser):
    return AnalyticsService(db).get_dashboard_stats()


@router.get("/trends/{machine_id}", response_model=MachineTrends)
def get_machine_trends(machine_id: int, db: DbSession, _: CurrentUser, hours: int = Query(24, ge=1, le=168)):
    if not MachineRepository(db).get(machine_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
    return AnalyticsService(db).get_machine_trends(machine_id, hours)


@router.get("/summary", response_model=AnalyticsSummary)
def get_analytics_summary(db: DbSession, _: CurrentUser):
    return AnalyticsService(db).get_analytics_summary()


@router.get("/dashboard/readings", response_model=list[SensorReadingResponse])
def get_dashboard_readings(db: DbSession, _: CurrentUser, limit: int = Query(10, ge=1, le=50)):
    return SensorReadingRepository(db).get_recent(limit=limit)


@router.get("/dashboard/alerts", response_model=list[AlertResponse])
def get_dashboard_alerts(db: DbSession, _: CurrentUser, limit: int = Query(10, ge=1, le=50)):
    return AlertRepository(db).get_recent(limit=limit)


@router.get("/dashboard/maintenance", response_model=list[MaintenanceResponse])
def get_dashboard_maintenance(db: DbSession, _: CurrentUser, limit: int = Query(10, ge=1, le=50)):
    return MaintenanceRepository(db).get_recent(limit=limit)


@router.get("/reports/{report_type}", response_class=PlainTextResponse)
def generate_report(report_type: str, db: DbSession, _: CurrentUser):
    summary = AnalyticsService(db).get_analytics_summary()
    dashboard = AnalyticsService(db).get_dashboard_stats()
    report_lines = [f"Ranbridge {report_type.title()} Report", "=" * 30]
    if report_type == "executive":
        report_lines.extend(
            [
                f"Average Health Score: {summary.machine_health_score}%",
                f"Machine Reliability: {summary.machine_reliability}%",
                f"Predicted Failures: {summary.predicted_failures}",
                f"Maintenance Cost Saved: ${summary.maintenance_cost_saved:.2f}",
                f"Downtime Prevented: {summary.downtime_prevented_hours:.2f} hours",
            ]
        )
    else:
        report_lines.extend(
            [
                f"Total Machines: {dashboard.total_machines}",
                f"Critical Machines: {dashboard.critical_machines}",
                f"Active Alerts: {dashboard.active_alerts}",
                f"Available Technicians: {dashboard.available_technicians}",
            ]
        )
    return "\n".join(report_lines)
