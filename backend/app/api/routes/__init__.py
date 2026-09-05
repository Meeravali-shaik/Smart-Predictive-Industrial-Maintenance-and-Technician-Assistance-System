"""API router aggregation."""

from fastapi import APIRouter

from app.api.routes import (
    ai,
    alerts,
    analytics,
    auth,
    machines,
    maintenance,
    notifications,
    predictions,
    sensor_readings,
    technicians,
    users,
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(machines.router)
api_router.include_router(sensor_readings.router)
api_router.include_router(predictions.router)
api_router.include_router(alerts.router)
api_router.include_router(technicians.router)
api_router.include_router(maintenance.router)
api_router.include_router(analytics.router)
api_router.include_router(notifications.router)
api_router.include_router(ai.router)
