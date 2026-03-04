from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: str  
    user_id: str
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True 