"""Dashboard and analytics aggregation service."""

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.machine import MachineStatus
from app.repositories.alert_repository import AlertRepository
from app.repositories.machine_repository import MachineRepository
from app.repositories.maintenance_repository import MaintenanceRepository
from app.repositories.prediction_repository import PredictionRepository
from app.repositories.sensor_reading_repository import SensorReadingRepository
from app.repositories.technician_repository import TechnicianRepository
from app.schemas import AnalyticsSummary, DashboardStats, MachineTrends, TrendPoint


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
        self.machine_repo = MachineRepository(db)
        self.alert_repo = AlertRepository(db)
        self.technician_repo = TechnicianRepository(db)
        self.sensor_repo = SensorReadingRepository(db)
        self.prediction_repo = PredictionRepository(db)
        self.maintenance_repo = MaintenanceRepository(db)

    def get_dashboard_stats(self) -> DashboardStats:
        machines = self.machine_repo.get_all(limit=1000)
        average_health = round(sum(m.health_score for m in machines) / len(machines), 2) if machines else 0.0
        predictions = self.prediction_repo.get_recent(limit=1000)
        predicted_failures = sum(1 for p in predictions if p.failure_probability >= 0.6)
        maintenance_cost = sum(float(p.estimated_maintenance_cost_usd or 0) for p in predictions if p.estimated_maintenance_cost_usd)
        downtime_prevented = sum(float(p.estimated_downtime_hours or 0) for p in predictions if p.estimated_downtime_hours)
        return DashboardStats(
            total_machines=self.machine_repo.count(),
            healthy_machines=self.machine_repo.count_by_status(MachineStatus.HEALTHY),
            warning_machines=self.machine_repo.count_by_status(MachineStatus.WARNING),
            critical_machines=self.machine_repo.count_by_status(MachineStatus.CRITICAL),
            active_alerts=self.alert_repo.get_active_count(),
            available_technicians=self.technician_repo.get_available_count(),
            offline_machines=self.machine_repo.count_by_status(MachineStatus.OFFLINE),
            maintenance_machines=self.machine_repo.count_by_status(MachineStatus.MAINTENANCE),
            average_health_score=average_health,
            predicted_failures=predicted_failures,
            maintenance_cost_saved=round(maintenance_cost, 2),
            downtime_prevented_hours=round(downtime_prevented, 2),
        )

    def get_machine_trends(self, machine_id: int, hours: int = 24) -> MachineTrends:
        since = datetime.now(timezone.utc) - timedelta(hours=hours)
        readings = self.sensor_repo.get_trends(machine_id, since)
        predictions = self.prediction_repo.get_trends_for_machine(machine_id)

        return MachineTrends(
            temperature=[TrendPoint(timestamp=r.recorded_at, value=r.temperature) for r in readings],
            vibration=[TrendPoint(timestamp=r.recorded_at, value=r.vibration) for r in readings],
            current=[TrendPoint(timestamp=r.recorded_at, value=r.current) for r in readings],
            health_score=[TrendPoint(timestamp=p.created_at, value=p.health_score) for p in predictions],
            failure_probability=[TrendPoint(timestamp=p.created_at, value=p.failure_probability * 100) for p in predictions],
        )

    def get_analytics_summary(self) -> AnalyticsSummary:
        machines = self.machine_repo.get_all(limit=1000)
        avg_health = sum(m.health_score for m in machines) / len(machines) if machines else 0

        all_averages = {"temperature": [], "current": [], "vibration": []}
        for machine in machines:
            avgs = self.sensor_repo.get_averages_for_machine(machine.id)
            all_averages["temperature"].append(avgs["average_temperature"])
            all_averages["current"].append(avgs["average_current"])
            all_averages["vibration"].append(avgs["average_vibration"])

        total_downtime = self.maintenance_repo.get_total_downtime()
        monthly_failures = self.maintenance_repo.get_monthly_failures()
        reliability = (avg_health / 100) * 100 if avg_health else 0
        savings = monthly_failures * 5000 + total_downtime * 250
        predictions = self.prediction_repo.get_recent(limit=1000)
        failure_distribution = {}
        for prediction in predictions:
            failure_distribution[prediction.failure_type] = failure_distribution.get(prediction.failure_type, 0) + 1
        critical_machines = [
            {"name": machine.name, "health_score": machine.health_score, "status": machine.status.value}
            for machine in sorted(machines, key=lambda item: item.health_score)[:5]
        ]
        frequent_faults = [
            {"name": fault, "count": count}
            for fault, count in sorted(failure_distribution.items(), key=lambda item: item[1], reverse=True)[:5]
        ]

        return AnalyticsSummary(
            machine_health_score=round(avg_health, 2),
            monthly_failures=monthly_failures,
            total_downtime_hours=round(total_downtime, 2),
            average_temperature=round(sum(all_averages["temperature"]) / len(all_averages["temperature"]) if all_averages["temperature"] else 0, 2),
            average_current=round(sum(all_averages["current"]) / len(all_averages["current"]) if all_averages["current"] else 0, 2),
            average_vibration=round(sum(all_averages["vibration"]) / len(all_averages["vibration"]) if all_averages["vibration"] else 0, 3),
            predictive_maintenance_savings=round(savings, 2),
            machine_reliability=round(reliability, 2),
            downtime_prevented_hours=round(sum(float(p.estimated_downtime_hours or 0) for p in predictions), 2),
            predicted_failures=sum(1 for p in predictions if p.failure_probability >= 0.6),
            maintenance_cost_saved=round(sum(float(p.estimated_maintenance_cost_usd or 0) for p in predictions), 2),
            failure_distribution=failure_distribution,
            critical_machines=critical_machines,
            frequent_faults=frequent_faults,
        )
