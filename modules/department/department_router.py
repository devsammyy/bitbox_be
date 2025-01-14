
from typing import List
from fastapi import APIRouter, HTTPException, status
from modules.db.database import db_dependency
from . import department_model
from modules.user import user_schema as user_pydantic
from modules.user import user_model

from modules.core.utils import get_password_hash


router = APIRouter()


@router.get("/users", status_code=status.HTTP_200_OK, response_model=List[user_pydantic.UserOut])
async def find_users(db: db_dependency):
    return db.query(department_model.User).all()


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=user_pydantic.UserOut)
async def find_user(user_id: str, db: db_dependency):
    return db.query(department_model.User).filter(department_model.User.id == user_id).first()


@router.post("/user/create", status_code=status.HTTP_201_CREATED, response_model=user_pydantic.UserOut)
async def create_user(user: user_pydantic.UserIn, db: db_dependency):
    user.full_name = user.first_name + " " + user.last_name
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    user.role = department_model.UserRole.MEMBER
    user_data = department_model.User(**user.model_dump())
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data


@router.put("/user/update/{user_id}", status_code=status.HTTP_200_OK, response_model=user_pydantic.UserOut)
async def update_user(user_id: str, user: user_pydantic.UserUpdateIn, db: db_dependency):
    user_query = db.query(department_model.User).filter(
        department_model.User.id == user_id)

    found_user = user_query.first()

    if not found_user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_query.update(user.model_dump(exclude_unset=True),
                      synchronize_session=False)
    db.commit()

    return user_query.first()


@router.delete("/user/delete/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: str, db: db_dependency):
    user_query = db.query(user_model.User).filter(
        department_model.User.id == user_id)

    found_user = user_query.first()

    if not found_user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "User deleted successfully"}
