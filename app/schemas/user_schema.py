from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=2000)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=2000)

class UserResponse(BaseModel):
    id: str 
    name: str
    email: EmailStr
    created_at: datetime

    class Config: 
        from_attributes = True