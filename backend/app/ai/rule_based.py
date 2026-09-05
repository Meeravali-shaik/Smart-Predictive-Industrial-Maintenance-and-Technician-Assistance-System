"""Rule-based predictive maintenance engine (Phase 1)."""

from dataclasses import dataclass
from typing import Optional

from app.models.prediction import PredictionSeverity
from app.models.sensor_reading import SensorReading


@dataclass
class PredictionResult:
    failure_type: str
    failure_probability: float
    health_score: float
    severity: PredictionSeverity
    remaining_useful_life_hours: float
    recommended_action: str
    prediction_method: str = "rule_based"


# Thresholds for industrial equipment monitoring
THRESHOLDS = {
    "temperature": {"warning": 75.0, "critical": 90.0},
    "vibration": {"warning": 5.0, "critical": 8.0},
    "current": {"warning": 15.0, "critical": 20.0},
    "humidity": {"warning": 70.0, "critical": 85.0},
    "pressure": {"warning": 120.0, "critical": 140.0},
    "rpm": {"warning_low": 800.0, "warning_high": 3200.0, "critical_high": 3500.0},
}


class RuleBasedPredictor:
    """Phase 1: Rule-based failure prediction using sensor thresholds and patterns."""

    def predict(self, reading: SensorReading) -> PredictionResult:
        temp = reading.temperature
        vib = reading.vibration
        curr = reading.current
        anomaly = reading.anomaly_type

        failure_type = "Normal Operation"
        failure_probability = 0.05
        severity = PredictionSeverity.LOW
        recommended_action = "Continue routine monitoring and scheduled maintenance."
        health_score = 100.0

        if anomaly == "bearing_failure" or (vib > THRESHOLDS["vibration"]["critical"] and temp > 70):
            failure_type = "Bearing Failure"
            failure_probability = 0.92
            severity = PredictionSeverity.CRITICAL
            health_score = 25.0
            recommended_action = (
                "Immediate shutdown recommended. Inspect bearings, check lubrication, "
                "and replace worn components."
            )
        elif anomaly == "motor_overheating" or temp > THRESHOLDS["temperature"]["critical"]:
            failure_type = "Motor Overheating"
            failure_probability = 0.88
            severity = PredictionSeverity.CRITICAL
            health_score = 30.0
            recommended_action = (
                "Reduce load, verify cooling system, inspect ventilation, and check motor insulation."
            )
        elif anomaly == "excessive_vibration" or vib > THRESHOLDS["vibration"]["critical"]:
            failure_type = "Excessive Vibration"
            failure_probability = 0.85
            severity = PredictionSeverity.HIGH
            health_score = 35.0
            recommended_action = "Check alignment, balance rotating parts, and inspect mounting bolts."
        elif anomaly == "power_overload" or curr > THRESHOLDS["current"]["critical"]:
            failure_type = "Power Overload"
            failure_probability = 0.80
            severity = PredictionSeverity.HIGH
            health_score = 40.0
            recommended_action = "Reduce electrical load, inspect power supply, and verify circuit breakers."
        elif anomaly == "sensor_failure":
            failure_type = "Sensor Malfunction"
            failure_probability = 0.60
            severity = PredictionSeverity.MEDIUM
            health_score = 55.0
            recommended_action = "Calibrate or replace faulty sensor. Verify data integrity before decisions."
        elif vib > THRESHOLDS["vibration"]["warning"] and temp > THRESHOLDS["temperature"]["warning"]:
            failure_type = "Early Bearing Wear"
            failure_probability = 0.65
            severity = PredictionSeverity.MEDIUM
            health_score = 60.0
            recommended_action = "Schedule bearing inspection within 72 hours. Monitor vibration trends."
        elif temp > THRESHOLDS["temperature"]["warning"]:
            failure_type = "Elevated Temperature"
            failure_probability = 0.45
            severity = PredictionSeverity.MEDIUM
            health_score = 70.0
            recommended_action = "Monitor cooling system and reduce operating temperature if possible."
        elif vib > THRESHOLDS["vibration"]["warning"]:
            failure_type = "Vibration Anomaly"
            failure_probability = 0.40
            severity = PredictionSeverity.LOW
            health_score = 75.0
            recommended_action = "Increase monitoring frequency and check for loose components."
        elif curr > THRESHOLDS["current"]["warning"]:
            failure_type = "Current Spike"
            failure_probability = 0.35
            severity = PredictionSeverity.LOW
            health_score = 78.0
            recommended_action = "Inspect electrical connections and verify load distribution."

        remaining_useful_life = self._estimate_rul(failure_probability, severity)

        return PredictionResult(
            failure_type=failure_type,
            failure_probability=round(failure_probability, 4),
            health_score=round(health_score, 2),
            severity=severity,
            remaining_useful_life_hours=remaining_useful_life,
            recommended_action=recommended_action,
        )

    def _estimate_rul(self, failure_probability: float, severity: PredictionSeverity) -> float:
        base_hours = {
            PredictionSeverity.LOW: 2000,
            PredictionSeverity.MEDIUM: 500,
            PredictionSeverity.HIGH: 120,
            PredictionSeverity.CRITICAL: 24,
        }
        multiplier = max(0.1, 1.0 - failure_probability)
        return round(base_hours[severity] * multiplier, 1)


def get_predictor(method: str = "rule_based") -> RuleBasedPredictor:
    """Factory for prediction engines. ML models can be plugged in here later."""
    if method == "rule_based":
        return RuleBasedPredictor()
    return RuleBasedPredictor()
