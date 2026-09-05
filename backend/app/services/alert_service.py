"""Alert generation, threshold monitoring, and technician auto-assignment."""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.ai.rule_based import THRESHOLDS
from app.models.alert import Alert, AlertSeverity, AlertStatus
from app.models.notification import Notification, NotificationType
from app.models.sensor_reading import SensorReading
from app.models.user import User, UserRole
from app.repositories.alert_repository import AlertRepository
from app.repositories.prediction_repository import PredictionRepository
from app.repositories.technician_repository import TechnicianRepository
from app.repositories.user_repository import UserRepository


class AlertService:
    FAILURE_PROBABILITY_THRESHOLD = 0.75

    def __init__(self, db: Session):
        self.db = db
        self.alert_repo = AlertRepository(db)
        self.technician_repo = TechnicianRepository(db)
        self.prediction_repo = PredictionRepository(db)
        self.user_repo = UserRepository(db)

    def evaluate_reading(self, reading: SensorReading) -> list[Alert]:
        alerts: list[Alert] = []

        checks = [
            ("temperature", reading.temperature, THRESHOLDS["temperature"]),
            ("vibration", reading.vibration, THRESHOLDS["vibration"]),
            ("current", reading.current, THRESHOLDS["current"]),
        ]

        for sensor_name, value, thresholds in checks:
            if value > thresholds["critical"]:
                alert = self._create_threshold_alert(
                    reading, sensor_name, value, thresholds["critical"], AlertSeverity.CRITICAL
                )
                if alert:
                    alerts.append(alert)
            elif value > thresholds["warning"]:
                alert = self._create_threshold_alert(
                    reading, sensor_name, value, thresholds["warning"], AlertSeverity.MEDIUM
                )
                if alert:
                    alerts.append(alert)

        latest_prediction = self.prediction_repo.get_latest_for_machine(reading.machine_id)
        if latest_prediction and latest_prediction.failure_probability >= self.FAILURE_PROBABILITY_THRESHOLD:
            alert = self._create_failure_probability_alert(reading, latest_prediction.failure_probability)
            if alert:
                alerts.append(alert)

        return alerts

    def _create_threshold_alert(
        self,
        reading: SensorReading,
        sensor_name: str,
        value: float,
        threshold: float,
        severity: AlertSeverity,
    ) -> Alert | None:
        existing = self.alert_repo.get_active_for_machine(reading.machine_id, f"{sensor_name}_threshold")
        if existing:
            return None

        title = f"{sensor_name.title()} Threshold Exceeded"
        message = f"{sensor_name.title()} reading {value:.2f} exceeded threshold {threshold:.2f}"
        recommended = self._get_recommended_action(sensor_name, severity)

        alert = Alert(
            machine_id=reading.machine_id,
            title=title,
            message=message,
            alert_type=f"{sensor_name}_threshold",
            severity=severity,
            status=AlertStatus.ACTIVE,
            threshold_value=threshold,
            actual_value=value,
            recommended_action=recommended,
        )

        if severity == AlertSeverity.CRITICAL:
            self._auto_assign_technician(alert)

        created = self.alert_repo.create(alert)
        self._notify_managers(created)
        return created

    def _create_failure_probability_alert(self, reading: SensorReading, probability: float) -> Alert | None:
        existing = self.alert_repo.get_active_for_machine(reading.machine_id, "failure_probability")
        if existing:
            return None

        alert = Alert(
            machine_id=reading.machine_id,
            title="High Failure Probability Detected",
            message=f"Failure probability reached {probability * 100:.1f}%",
            alert_type="failure_probability",
            severity=AlertSeverity.HIGH if probability < 0.9 else AlertSeverity.CRITICAL,
            status=AlertStatus.ACTIVE,
            threshold_value=self.FAILURE_PROBABILITY_THRESHOLD,
            actual_value=probability,
            recommended_action="Schedule predictive maintenance inspection immediately.",
        )

        if alert.severity == AlertSeverity.CRITICAL:
            self._auto_assign_technician(alert)

        created = self.alert_repo.create(alert)
        self._notify_managers(created)
        return created

    def _auto_assign_technician(self, alert: Alert) -> None:
        skill_map = {
            "temperature_threshold": "thermal",
            "vibration_threshold": "mechanical",
            "current_threshold": "electrical",
            "failure_probability": "predictive",
        }
        skill = skill_map.get(alert.alert_type, None)
        technician = self.technician_repo.get_available_technician(skill, specialization=alert.title.lower())
        if technician:
            alert.technician_id = technician.id
            alert.is_auto_assigned = True
            technician.availability = "busy"
            technician.current_workload = (technician.current_workload or 0) + 1
            technician.assignment_count = (technician.assignment_count or 0) + 1
            technician.last_assigned_at = datetime.now(timezone.utc)
            self.db.add(technician)

    def _notify_managers(self, alert: Alert) -> None:
        managers = self.db.query(User).filter(
            User.role.in_([UserRole.ADMIN, UserRole.FACTORY_MANAGER]),
            User.is_active.is_(True),
        ).all()
        for manager in managers:
            notification = Notification(
                user_id=manager.id,
                title=alert.title,
                message=alert.message,
                notification_type=NotificationType.ALERT,
                reference_id=alert.id,
            )
            self.db.add(notification)
        self.db.commit()

    @staticmethod
    def _get_recommended_action(sensor_name: str, severity: AlertSeverity) -> str:
        actions = {
            "temperature": "Check cooling systems and reduce operating load.",
            "vibration": "Inspect bearings, alignment, and mounting hardware.",
            "current": "Verify electrical load and inspect power circuits.",
        }
        base = actions.get(sensor_name, "Investigate sensor readings immediately.")
        if severity == AlertSeverity.CRITICAL:
            return f"CRITICAL: {base} Consider immediate shutdown."
        return base

    def resolve_alert(self, alert: Alert) -> Alert:
        alert.status = AlertStatus.RESOLVED
        alert.resolved_at = datetime.now(timezone.utc)
        return self.alert_repo.update(alert)

    def acknowledge_alert(self, alert: Alert) -> Alert:
        alert.status = AlertStatus.ACKNOWLEDGED
        return self.alert_repo.update(alert)
