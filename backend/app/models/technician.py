"""Technician ORM model."""

import enum
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class AvailabilityStatus(str, enum.Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFF_DUTY = "off_duty"


class Technician(Base):
    __tablename__ = "technicians"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    skills: Mapped[str] = mapped_column(Text, nullable=False)
    specialization: Mapped[str | None] = mapped_column(String(100), nullable=True)
    current_workload: Mapped[int] = mapped_column(Integer, default=0)
    assignment_count: Mapped[int] = mapped_column(Integer, default=0)
    availability: Mapped[AvailabilityStatus] = mapped_column(
        Enum(AvailabilityStatus), default=AvailabilityStatus.AVAILABLE
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_assigned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", back_populates="technician_profile")
    assigned_alerts = relationship("Alert", back_populates="technician")
    maintenance_records = relationship("MaintenanceHistory", back_populates="technician")
