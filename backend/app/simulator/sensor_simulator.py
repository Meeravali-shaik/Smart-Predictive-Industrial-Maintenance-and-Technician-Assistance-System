"""Sensor data simulator - replaces physical IoT devices in MVP."""

import random
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.session import SessionLocal
from app.models.machine import Machine, MachineStatus
from app.models.sensor_reading import SensorReading
from app.repositories.machine_repository import MachineRepository
from app.services.alert_service import AlertService
from app.services.prediction_service import PredictionService

settings = get_settings()

ANOMALY_TYPES = [
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    "bearing_failure",
    "motor_overheating",
    "excessive_vibration",
    "power_overload",
    "sensor_failure",
]


@dataclass
class MachineSimulatorState:
    """Per-machine baseline and anomaly state for realistic simulation."""
    base_temperature: float = 55.0
    base_vibration: float = 2.5
    base_current: float = 10.0
    base_humidity: float = 45.0
    base_pressure: float = 100.0
    base_rpm: float = 2400.0
    active_anomaly: Optional[str] = None
    anomaly_ticks: int = 0


class SensorSimulator:
    """
    Background sensor simulator service.
    Designed to be swappable with MQTT/ESP32/PLC ingestion without changing business logic.
    """

    def __init__(self):
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._machine_states: Dict[int, MachineSimulatorState] = {}

    def start(self) -> None:
        if self._running or not settings.SIMULATOR_ENABLED:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def _run_loop(self) -> None:
        while self._running:
            try:
                self._simulate_cycle()
            except Exception as exc:
                print(f"[Simulator] Error in cycle: {exc}")
            time.sleep(settings.SIMULATOR_INTERVAL_SECONDS)

    def _simulate_cycle(self) -> None:
        db = SessionLocal()
        try:
            machines = MachineRepository(db).get_all(limit=100)
            for machine in machines:
                if machine.status == MachineStatus.OFFLINE:
                    continue
                reading = self._generate_reading(machine)
                db.add(reading)
                db.commit()
                db.refresh(reading)

                prediction_service = PredictionService(db)
                prediction_service.process_reading(reading)

                alert_service = AlertService(db)
                alert_service.evaluate_reading(reading)
        finally:
            db.close()

    def _get_state(self, machine_id: int) -> MachineSimulatorState:
        if machine_id not in self._machine_states:
            self._machine_states[machine_id] = MachineSimulatorState(
                base_temperature=random.uniform(50, 60),
                base_vibration=random.uniform(2.0, 3.5),
                base_current=random.uniform(8, 12),
                base_humidity=random.uniform(40, 55),
                base_pressure=random.uniform(95, 105),
                base_rpm=random.uniform(2200, 2600),
            )
        return self._machine_states[machine_id]

    def _generate_reading(self, machine: Machine) -> SensorReading:
        state = self._get_state(machine.id)

        # Occasionally inject anomalies
        if state.active_anomaly is None and random.random() < 0.08:
            state.active_anomaly = random.choice(ANOMALY_TYPES[7:])
            state.anomaly_ticks = random.randint(3, 15)

        anomaly = state.active_anomaly
        if state.anomaly_ticks > 0:
            state.anomaly_ticks -= 1
            if state.anomaly_ticks == 0:
                state.active_anomaly = None
                anomaly = state.active_anomaly

        temp = self._noise(state.base_temperature, 1.5)
        vib = self._noise(state.base_vibration, 0.3)
        curr = self._noise(state.base_current, 0.5)
        humidity = self._noise(state.base_humidity, 2.0)
        pressure = self._noise(state.base_pressure, 1.5)
        rpm = self._noise(state.base_rpm, 50)

        if anomaly == "bearing_failure":
            vib += random.uniform(5, 8)
            temp += random.uniform(8, 15)
        elif anomaly == "motor_overheating":
            temp += random.uniform(25, 40)
            curr += random.uniform(3, 6)
        elif anomaly == "excessive_vibration":
            vib += random.uniform(6, 10)
        elif anomaly == "power_overload":
            curr += random.uniform(8, 12)
            rpm += random.uniform(100, 300)
        elif anomaly == "sensor_failure":
            if random.random() < 0.5:
                temp = -999.0
            else:
                vib = random.uniform(50, 100)

        return SensorReading(
            machine_id=machine.id,
            temperature=round(max(temp, 0), 2),
            vibration=round(max(vib, 0), 3),
            current=round(max(curr, 0), 2),
            humidity=round(max(min(humidity, 100), 0), 2),
            pressure=round(max(pressure, 0), 2),
            rpm=round(max(rpm, 0), 0),
            anomaly_type=anomaly,
            recorded_at=datetime.now(timezone.utc),
        )

    @staticmethod
    def _noise(base: float, variance: float) -> float:
        return base + random.uniform(-variance, variance)


# Singleton simulator instance
simulator = SensorSimulator()
