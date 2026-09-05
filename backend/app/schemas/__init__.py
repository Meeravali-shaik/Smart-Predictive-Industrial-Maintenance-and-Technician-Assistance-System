"""Shared Pydantic schemas and enums."""

from datetime import date, datetime
from enum import Enum
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRole(str, Enum):
    ADMIN = "admin"
    FACTORY_MANAGER = "factory_manager"
    TECHNICIAN = "technician"


class MachineStatus(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class PredictionSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AvailabilityStatus(str, Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFF_DUTY = "off_duty"


class NotificationType(str, Enum):
    ALERT = "alert"
    MAINTENANCE = "maintenance"
    SYSTEM = "system"
    PREDICTION = "prediction"


class NotificationStatus(str, Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int


class MessageResponse(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[UserRole] = None


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)
    full_name: str = Field(min_length=1, max_length=255)
    role: UserRole = UserRole.TECHNICIAN


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=128)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(default=None, min_length=3, max_length=100)
    full_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(default=None, min_length=6, max_length=128)


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class MachineBase(BaseModel):
    machine_id: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=255)
    factory: str = Field(min_length=1, max_length=255)
    location: str = Field(min_length=1, max_length=255)
    machine_type: str = Field(min_length=1, max_length=100)
    installation_date: date
    description: Optional[str] = None


class MachineCreate(MachineBase):
    status: MachineStatus = MachineStatus.HEALTHY
    health_score: float = Field(default=100.0, ge=0, le=100)


class MachineUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    factory: Optional[str] = None
    location: Optional[str] = None
    machine_type: Optional[str] = None
    installation_date: Optional[date] = None
    status: Optional[MachineStatus] = None
    health_score: Optional[float] = Field(default=None, ge=0, le=100)
    description: Optional[str] = None


class MachineResponse(MachineBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: MachineStatus
    health_score: float
    created_at: datetime
    updated_at: datetime


class SensorReadingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    machine_id: int
    temperature: float
    vibration: float
    current: float
    humidity: float
    pressure: float
    rpm: float
    anomaly_type: Optional[str] = None
    recorded_at: datetime


class PredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    machine_id: int
    failure_type: str
    failure_probability: float
    health_score: float
    severity: PredictionSeverity
    remaining_useful_life_hours: float
    remaining_useful_life_days: float = 0.0
    confidence: Optional[float] = None
    explanation: Optional[str] = None
    risk_level: Optional[str] = None
    maintenance_recommendation: Optional[str] = None
    estimated_maintenance_duration_hours: Optional[float] = None
    estimated_downtime_hours: Optional[float] = None
    estimated_maintenance_cost_usd: Optional[float] = None
    prediction_method: str
    recommended_action: Optional[str] = None
    created_at: datetime


class AlertCreate(BaseModel):
    machine_id: int
    title: str
    message: str
    alert_type: str
    severity: AlertSeverity
    threshold_value: Optional[float] = None
    actual_value: Optional[float] = None
    recommended_action: Optional[str] = None


class AlertUpdate(BaseModel):
    status: Optional[AlertStatus] = None
    technician_id: Optional[int] = None
    recommended_action: Optional[str] = None


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    machine_id: int
    technician_id: Optional[int] = None
    title: str
    message: str
    alert_type: str
    severity: AlertSeverity
    status: AlertStatus
    threshold_value: Optional[float] = None
    actual_value: Optional[float] = None
    recommended_action: Optional[str] = None
    is_auto_assigned: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None


class TechnicianBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    phone: str = Field(min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    skills: str
    specialization: Optional[str] = None
    current_workload: int = 0
    assignment_count: int = 0
    availability: AvailabilityStatus = AvailabilityStatus.AVAILABLE


class TechnicianCreate(TechnicianBase):
    user_id: Optional[int] = None


class TechnicianUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    skills: Optional[str] = None
    specialization: Optional[str] = None
    current_workload: Optional[int] = None
    assignment_count: Optional[int] = None
    availability: Optional[AvailabilityStatus] = None
    is_active: Optional[bool] = None


class TechnicianResponse(TechnicianBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: Optional[int] = None
    is_active: bool
    created_at: datetime


class MaintenanceCreate(BaseModel):
    machine_id: int
    technician_id: Optional[int] = None
    issue: str
    repair_date: datetime
    repair_notes: Optional[str] = None
    parts_replaced: Optional[str] = None
    downtime_hours: float = 0.0
    status: str = "completed"


class MaintenanceUpdate(BaseModel):
    technician_id: Optional[int] = None
    issue: Optional[str] = None
    repair_date: Optional[datetime] = None
    repair_notes: Optional[str] = None
    parts_replaced: Optional[str] = None
    downtime_hours: Optional[float] = None
    status: Optional[str] = None


class MaintenanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    machine_id: int
    technician_id: Optional[int] = None
    issue: str
    repair_date: datetime
    repair_notes: Optional[str] = None
    parts_replaced: Optional[str] = None
    downtime_hours: float
    status: str
    created_at: datetime


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    message: str
    notification_type: NotificationType
    is_read: bool
    status: NotificationStatus
    reference_id: Optional[int] = None
    created_at: datetime


class DashboardStats(BaseModel):
    total_machines: int
    healthy_machines: int
    warning_machines: int
    critical_machines: int
    active_alerts: int
    available_technicians: int
    offline_machines: int
    maintenance_machines: int
    average_health_score: float = 0.0
    predicted_failures: int = 0
    maintenance_cost_saved: float = 0.0
    downtime_prevented_hours: float = 0.0


class TrendPoint(BaseModel):
    timestamp: datetime
    value: float


class MachineTrends(BaseModel):
    temperature: List[TrendPoint]
    vibration: List[TrendPoint]
    current: List[TrendPoint]
    health_score: List[TrendPoint]
    failure_probability: List[TrendPoint]


class AnalyticsSummary(BaseModel):
    machine_health_score: float
    monthly_failures: int
    total_downtime_hours: float
    average_temperature: float
    average_current: float
    average_vibration: float
    predictive_maintenance_savings: float
    machine_reliability: float
    downtime_prevented_hours: float = 0.0
    predicted_failures: int = 0
    maintenance_cost_saved: float = 0.0
    failure_distribution: dict = {}
    critical_machines: list[dict] = []
    frequent_faults: list[dict] = []


class TechnicianAssistanceResponse(BaseModel):
    alert: AlertResponse
    machine: MachineResponse
    technician: Optional[TechnicianResponse] = None
    fault: str
    priority: str
    recommended_action: str
    maintenance_history: List[MaintenanceResponse]
