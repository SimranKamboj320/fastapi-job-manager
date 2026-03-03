from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: str

class ProjectResponse(BaseModel):
    id: str  
    user_id: str
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True 