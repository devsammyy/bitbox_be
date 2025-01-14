from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel
from ..user.user_model import UserRole


class UserIn(BaseModel):
    first_name: str
    last_name: str
    username: str
    full_name: Optional[str] = None
    email: str
    role: Optional[UserRole] = None
    gender: str
    password: str
    phone_number: str

    class Config:
        from_attributes = True
        extra = "ignore"


class UserOut(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    username: str
    full_name: str
    email: str
    phone_number: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdateIn(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True
