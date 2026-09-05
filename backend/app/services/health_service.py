"""Health score and degradation analysis utilities for machines."""

from __future__ import annotations

from dataclasses import dataclass

from app.models.machine import Machine
from app.models.sensor_reading import SensorReading


@dataclass
class HealthAssessment:
    score: float
    band: str
    degradation_factor: float
    explanation: str


class HealthScoreEngine:
    """Heuristic health scoring engine for predictive maintenance."""

    def calculate(self, machine: Machine, reading: SensorReading, history_count: int = 0) -> HealthAssessment:
        temp_penalty = max(0.0, (reading.temperature - 70.0) / 20.0) * 25.0
        vibration_penalty = max(0.0, (reading.vibration - 3.0) / 4.0) * 25.0
        current_penalty = max(0.0, (reading.current - 12.0) / 8.0) * 20.0
        pressure_penalty = max(0.0, (reading.pressure - 100.0) / 40.0) * 10.0
        humidity_penalty = max(0.0, (reading.humidity - 55.0) / 30.0) * 8.0
        rpm_penalty = max(0.0, abs(reading.rpm - 2400.0) / 2400.0) * 8.0

        degradation_factor = min(0.25, max(0.0, history_count / 100.0))
        degradation_penalty = degradation_factor * 20.0

        score = 100.0 - temp_penalty - vibration_penalty - current_penalty - pressure_penalty - humidity_penalty - rpm_penalty - degradation_penalty
        score = max(0.0, min(100.0, round(score, 2)))

        if score < 40:
            band = "emergency"
        elif score < 60:
            band = "critical"
        elif score < 80:
            band = "warning"
        else:
            band = "healthy"

        explanation = self._build_explanation(score, reading)
        return HealthAssessment(score=score, band=band, degradation_factor=round(degradation_factor, 3), explanation=explanation)

    def _build_explanation(self, score: float, reading: SensorReading) -> str:
        issues = []
        if reading.temperature > 75:
            issues.append("temperature elevation")
        if reading.vibration > 5:
            issues.append("elevated vibration")
        if reading.current > 15:
            issues.append("current surge")
        if reading.pressure > 120 or reading.humidity > 70:
            issues.append("environmental stress")
        if not issues:
            return "Operating within expected thresholds with mild drift from baseline conditions."
        return f"Primary contributors: {', '.join(issues)}."
