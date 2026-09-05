"""Prediction service orchestrating AI engines and machine health updates."""

from sqlalchemy.orm import Session

from app.ai.rule_based import get_predictor
from app.models.machine import MachineStatus
from app.models.prediction import Prediction
from app.models.sensor_reading import SensorReading
from app.repositories.machine_repository import MachineRepository
from app.repositories.prediction_repository import PredictionRepository
from app.repositories.sensor_reading_repository import SensorReadingRepository
from app.services.health_service import HealthScoreEngine
from app.services.notification_service import NotificationService
from app.services.recommendation_service import RecommendationEngine
from app.models.notification import NotificationType


class PredictionService:
    def __init__(self, db: Session):
        self.db = db
        self.prediction_repo = PredictionRepository(db)
        self.machine_repo = MachineRepository(db)
        self.sensor_repo = SensorReadingRepository(db)
        self.predictor = get_predictor("rule_based")
        self.health_engine = HealthScoreEngine()
        self.recommendation_engine = RecommendationEngine()
        self.notification_service = NotificationService(db)

    def process_reading(self, reading: SensorReading) -> Prediction:
        result = self.predictor.predict(reading)
        history_count = len(self.sensor_repo.get_trends(reading.machine_id, since=None)) if False else 0
        assessment = self.health_engine.calculate(self.machine_repo.get(reading.machine_id), reading, history_count)
        recommendation = self.recommendation_engine.build(result.failure_type, result.severity.value, assessment.score)

        prediction = Prediction(
            machine_id=reading.machine_id,
            failure_type=result.failure_type,
            failure_probability=result.failure_probability,
            health_score=assessment.score,
            severity=result.severity,
            remaining_useful_life_hours=result.remaining_useful_life_hours,
            remaining_useful_life_days=round(result.remaining_useful_life_hours / 24.0, 2),
            confidence=round(result.failure_probability, 2),
            explanation=assessment.explanation + f" | Fault signal: {result.failure_type}",
            risk_level=assessment.band.upper(),
            maintenance_recommendation=recommendation.title,
            estimated_maintenance_duration_hours=recommendation.estimated_duration_hours,
            estimated_downtime_hours=recommendation.estimated_downtime_hours,
            estimated_maintenance_cost_usd=recommendation.estimated_cost_usd,
            prediction_method=result.prediction_method,
            recommended_action=result.recommended_action,
        )
        created = self.prediction_repo.create(prediction)

        machine = self.machine_repo.get(reading.machine_id)
        if machine:
            machine.health_score = assessment.score
            if assessment.band == "emergency":
                machine.status = MachineStatus.CRITICAL
            elif assessment.band == "critical":
                machine.status = MachineStatus.CRITICAL
            elif assessment.band == "warning":
                machine.status = MachineStatus.WARNING
            else:
                machine.status = MachineStatus.HEALTHY if machine.status != MachineStatus.MAINTENANCE else MachineStatus.MAINTENANCE
            self.machine_repo.update(machine)

        if result.failure_probability >= 0.6:
            self.notification_service.create_for_roles(
                title="Prediction generated",
                message=f"{result.failure_type} predicted for machine {reading.machine_id}",
                notification_type=NotificationType.PREDICTION,
                roles=["admin", "factory_manager"],
                reference_id=created.id,
            )

        return created
