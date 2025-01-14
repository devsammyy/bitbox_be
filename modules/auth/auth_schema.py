from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel

from ..user.user_schema import UserOut


class TokenIn(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: str


class TokenOut(BaseModel):
    access_token: str
    user: UserOut

    class Config:
        from_attributes = True
