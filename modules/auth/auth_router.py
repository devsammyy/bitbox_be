
from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..auth.auth_schema import TokenIn, TokenOut
from ..db.database import db_dependency
from ..user.user_model import User, UserRole
from ..user.user_schema import UserOut, UserIn, UserUpdateIn
from ..core.utils import create_access_token, get_password_hash, verify_password
from dotenv import load_dotenv
import os
load_dotenv()

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenOut)
async def login(db: db_dependency, user_payload: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.username ==
                                 user_payload.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    password_verified = verify_password(
        user_payload.password, user.password)

    if not password_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return TokenOut(user=user, access_token=access_token)
