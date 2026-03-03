from typing import Optional, Dict, Any
from enum import Enum

class PriorityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class StatusEnum(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING" 
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
 
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
    result: Optional[str] # string or none
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True