"""Prediction ORM model."""

import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class PredictionSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machines.id", ondelete="CASCADE"), index=True)
    failure_type: Mapped[str] = mapped_column(String(255), nullable=False)
    failure_probability: Mapped[float] = mapped_column(Float, nullable=False)
    health_score: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[PredictionSeverity] = mapped_column(Enum(PredictionSeverity), nullable=False)
    remaining_useful_life_hours: Mapped[float] = mapped_column(Float, nullable=False)
    remaining_useful_life_days: Mapped[float] = mapped_column(Float, default=0.0)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    risk_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    maintenance_recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)
    estimated_maintenance_duration_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    estimated_downtime_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    estimated_maintenance_cost_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    prediction_method: Mapped[str] = mapped_column(String(50), default="rule_based")
    recommended_action: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )

    machine = relationship("Machine", back_populates="predictions")
