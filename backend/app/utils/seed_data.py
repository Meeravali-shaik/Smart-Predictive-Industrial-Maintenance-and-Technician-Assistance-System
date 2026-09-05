"""Sample data seeding for development and demo."""

from datetime import date, datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.machine import Machine, MachineStatus
from app.models.maintenance_history import MaintenanceHistory
from app.models.technician import AvailabilityStatus, Technician
from app.models.user import User, UserRole


def seed_sample_data(db: Session) -> None:
    if db.query(User).count() > 0:
        return

    users = [
        User(
            email="admin@industrial.com",
            username="admin",
            full_name="System Administrator",
            role=UserRole.ADMIN,
            hashed_password=get_password_hash("admin123"),
        ),
        User(
            email="manager@industrial.com",
            username="manager",
            full_name="Factory Manager",
            role=UserRole.FACTORY_MANAGER,
            hashed_password=get_password_hash("manager123"),
        ),
        User(
            email="tech@industrial.com",
            username="technician",
            full_name="John Technician",
            role=UserRole.TECHNICIAN,
            hashed_password=get_password_hash("tech123"),
        ),
    ]
    db.add_all(users)
    db.flush()

    technicians = [
        Technician(
            user_id=users[2].id,
            name="John Technician",
            phone="+1-555-0101",
            email="tech@industrial.com",
            skills="mechanical,electrical,predictive,thermal",
            availability=AvailabilityStatus.AVAILABLE,
        ),
        Technician(
            name="Sarah Martinez",
            phone="+1-555-0102",
            email="sarah@industrial.com",
            skills="mechanical,vibration,alignment",
            availability=AvailabilityStatus.AVAILABLE,
        ),
        Technician(
            name="Mike Chen",
            phone="+1-555-0103",
            email="mike@industrial.com",
            skills="electrical,power,controls",
            availability=AvailabilityStatus.BUSY,
        ),
        Technician(
            name="Lisa Johnson",
            phone="+1-555-0104",
            email="lisa@industrial.com",
            skills="thermal,cooling,HVAC",
            availability=AvailabilityStatus.AVAILABLE,
        ),
    ]
    db.add_all(technicians)

    machines = [
        Machine(
            machine_id="CNC-001",
            name="CNC Milling Machine Alpha",
            factory="North Plant",
            location="Building A - Floor 1",
            machine_type="CNC Milling",
            installation_date=date(2020, 3, 15),
            status=MachineStatus.HEALTHY,
            health_score=95.0,
            description="High-precision 5-axis CNC milling machine",
        ),
        Machine(
            machine_id="CONV-002",
            name="Conveyor Belt System Beta",
            factory="North Plant",
            location="Building A - Floor 2",
            machine_type="Conveyor",
            installation_date=date(2019, 7, 22),
            status=MachineStatus.HEALTHY,
            health_score=88.0,
            description="Main production line conveyor system",
        ),
        Machine(
            machine_id="PUMP-003",
            name="Hydraulic Pump Gamma",
            factory="South Plant",
            location="Building B - Basement",
            machine_type="Hydraulic Pump",
            installation_date=date(2018, 11, 5),
            status=MachineStatus.HEALTHY,
            health_score=92.0,
            description="Primary hydraulic pump for press operations",
        ),
        Machine(
            machine_id="COMP-004",
            name="Air Compressor Delta",
            factory="South Plant",
            location="Building B - Floor 1",
            machine_type="Compressor",
            installation_date=date(2021, 1, 10),
            status=MachineStatus.HEALTHY,
            health_score=90.0,
            description="Industrial air compressor unit",
        ),
        Machine(
            machine_id="ROBOT-005",
            name="Assembly Robot Epsilon",
            factory="East Plant",
            location="Building C - Floor 1",
            machine_type="Robotic Arm",
            installation_date=date(2022, 6, 18),
            status=MachineStatus.HEALTHY,
            health_score=97.0,
            description="6-axis robotic assembly arm",
        ),
        Machine(
            machine_id="FURN-006",
            name="Industrial Furnace Zeta",
            factory="East Plant",
            location="Building C - Floor 2",
            machine_type="Furnace",
            installation_date=date(2017, 9, 30),
            status=MachineStatus.HEALTHY,
            health_score=85.0,
            description="Heat treatment furnace",
        ),
    ]
    db.add_all(machines)
    db.flush()

    maintenance_records = [
        MaintenanceHistory(
            machine_id=machines[0].id,
            technician_id=technicians[0].id,
            issue="Routine bearing lubrication",
            repair_date=datetime.now(timezone.utc) - timedelta(days=30),
            repair_notes="Applied high-temperature grease to all bearing points",
            parts_replaced="Bearing grease",
            downtime_hours=2.0,
        ),
        MaintenanceHistory(
            machine_id=machines[2].id,
            technician_id=technicians[1].id,
            issue="Hydraulic seal replacement",
            repair_date=datetime.now(timezone.utc) - timedelta(days=15),
            repair_notes="Replaced worn hydraulic seals on main pump",
            parts_replaced="Hydraulic seal kit",
            downtime_hours=4.5,
        ),
        MaintenanceHistory(
            machine_id=machines[4].id,
            technician_id=technicians[2].id,
            issue="Motor controller calibration",
            repair_date=datetime.now(timezone.utc) - timedelta(days=7),
            repair_notes="Recalibrated servo motors and updated firmware",
            parts_replaced=None,
            downtime_hours=1.5,
        ),
    ]
    db.add_all(maintenance_records)
    db.commit()
