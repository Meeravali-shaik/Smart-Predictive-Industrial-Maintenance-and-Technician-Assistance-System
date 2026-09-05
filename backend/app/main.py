"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.routes import api_router
from app.core.config import get_settings
from app.database.base import Base
from app.database.session import engine, SessionLocal
from app.simulator.sensor_simulator import simulator
from app.utils.seed_data import seed_sample_data

settings = get_settings()
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT])


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_sample_data(db)
    finally:
        db.close()
    simulator.start()
    yield
    simulator.stop()


app = FastAPI(
    title=settings.APP_NAME,
    description="Smart Predictive Industrial Maintenance and Technician Assistance System",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
@limiter.limit(settings.RATE_LIMIT)
def health_check(request: Request):
    return {"status": "healthy", "app": settings.APP_NAME, "simulator": settings.SIMULATOR_ENABLED}


app.include_router(api_router)
