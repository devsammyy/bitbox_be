
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from ..auth.auth_schema import TokenData
from ..user.user_model import User
from ..db.database import db_dependency
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import os
from typing import Annotated
import jwt
from dotenv import load_dotenv
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: int):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv(
        "SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized user",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"),
                             algorithms=[os.getenv("ALGORITHM")])
        username = TokenData(username=payload.get("sub"))
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username.username).first()
    return user
