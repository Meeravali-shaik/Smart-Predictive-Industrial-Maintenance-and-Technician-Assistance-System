"""Maintenance history ORM model."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class MaintenanceHistory(Base):
    __tablename__ = "maintenance_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machines.id", ondelete="CASCADE"), index=True)
    technician_id: Mapped[int | None] = mapped_column(
        ForeignKey("technicians.id", ondelete="SET NULL"), nullable=True
    )
    issue: Mapped[str] = mapped_column(Text, nullable=False)
    repair_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    repair_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    parts_replaced: Mapped[str | None] = mapped_column(Text, nullable=True)
    downtime_hours: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(50), default="completed")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    machine = relationship("Machine", back_populates="maintenance_records")
    technician = relationship("Technician", back_populates="maintenance_records")
