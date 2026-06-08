from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    gender: str
    email: EmailStr
    balance: float
    is_active: bool


class UserResponse(BaseModel):
    public_id: str
    first_name: str
    last_name: str
    gender: str
    email: str
    balance: float
    is_active: bool

    class Config:
        from_attributes = True