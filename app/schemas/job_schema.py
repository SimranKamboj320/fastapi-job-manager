from typing import Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class PriorityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class StatusEnum(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"


class SortByEnum(str, Enum):
    created_at = "created_at"
    priority = "priority"


class OrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class JobCreate(BaseModel):
    name: str
    payload: Dict[str, Any]
    priority: PriorityEnum


class JobResponse(BaseModel):
    id: str
    project_id: str
    name: str
    payload: Dict[str, Any]
    priority: PriorityEnum
    status: StatusEnum
    result: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnalyticsResponse(BaseModel):
    total_projects: int
    total_jobs: int
    completed: int
    failed: int
    pending: int
    high_priority: int


class JobQueryParams(BaseModel):
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
    page: int = 1
    limit: int = 10
    sort_by: SortByEnum = SortByEnum.created_at
    order: OrderEnum = OrderEnum.asc