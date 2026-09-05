"""Maintenance recommendation engine for predicted faults."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class MaintenanceRecommendation:
    title: str
    steps: List[str]
    estimated_duration_hours: float
    estimated_downtime_hours: float
    estimated_cost_usd: float
    priority: str


class RecommendationEngine:
    """Heuristic maintenance planning engine."""

    def build(self, fault_type: str, severity: str, health_score: float) -> MaintenanceRecommendation:
        recommendations = {
            "Bearing Failure": {
                "steps": [
                    "Lubricate the bearing assembly",
                    "Inspect shaft alignment and mounting",
                    "Replace the damaged bearing if wear is confirmed",
                ],
                "duration": 6.0,
                "downtime": 8.0,
                "cost": 4200.0,
                "priority": "high",
            },
            "Motor Overheating": {
                "steps": [
                    "Reduce operating load and verify cooling flow",
                    "Inspect motor insulation and ventilation",
                    "Replace overheating components if needed",
                ],
                "duration": 5.0,
                "downtime": 6.0,
                "cost": 3200.0,
                "priority": "high",
            },
            "Power Overload": {
                "steps": [
                    "Inspect electrical load distribution",
                    "Check breaker settings and power circuits",
                    "Rebalance load or replace affected hardware",
                ],
                "duration": 4.0,
                "downtime": 5.0,
                "cost": 2500.0,
                "priority": "medium",
            },
        }

        fallback = {
            "steps": [
                "Inspect the machine for abnormal operating conditions",
                "Verify sensor integrity before dispatching maintenance",
                "Plan corrective intervention based on observed trends",
            ],
            "duration": 3.0,
            "downtime": 4.0,
            "cost": 1800.0,
            "priority": "medium",
        }

        config = recommendations.get(fault_type, fallback)
        if health_score < 50:
            config = {
                **config,
                "priority": "critical",
                "duration": round(config["duration"] + 2.0, 1),
                "downtime": round(config["downtime"] + 3.0, 1),
                "cost": round(config["cost"] + 1200.0, 2),
            }
        elif severity == "low":
            config = {
                **config,
                "priority": "low",
                "duration": round(config["duration"] - 1.0, 1),
            }
        return MaintenanceRecommendation(
            title=f"{fault_type} Maintenance Plan",
            steps=config["steps"],
            estimated_duration_hours=float(config["duration"]),
            estimated_downtime_hours=float(config["downtime"]),
            estimated_cost_usd=float(config["cost"]),
            priority=str(config["priority"]),
        )
