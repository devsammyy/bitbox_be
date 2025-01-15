
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from ..db.database import db_dependency
from ..core import utils
from ..user.user_model import User, UserRole
from ..user.user_schema import UserOut, UserIn, UserUpdateIn
from ..core.utils import get_password_hash


router = APIRouter()


@router.get("/users", status_code=status.HTTP_200_OK, response_model=List[UserOut])
async def find_users(db: db_dependency, current_user: int = Depends(utils.get_current_user)):
    print(current_user)
    return db.query(User).all()


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def find_user(user_id: str, db: db_dependency, current_user: int = Depends(utils.get_current_user)):
    return db.query(User).filter(User.id == user_id).first()


@router.post("/user/create", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: UserIn, db: db_dependency):
    existing_user = db.query(User).filter(
        User.username == user.username).first()
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    user.full_name = user.first_name + " " + user.last_name
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    user.role = UserRole.MEMBER
    user_data = User(**user.model_dump())
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data


@router.put("/user/update/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def update_user(user_id: str, user: UserUpdateIn, db: db_dependency, current_user: int = Depends(utils.get_current_user)):
    user_query = db.query(User).filter(
        User.id == user_id)

    found_user = user_query.first()

    if not found_user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_query.update(user.model_dump(exclude_unset=True),
                      synchronize_session=False)
    db.commit()

    return user_query.first()


@router.delete("/user/delete/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: str, db: db_dependency, current_user: int = Depends(utils.get_current_user)):
    user_query = db.query(User).filter(
        User.id == user_id)

    found_user = user_query.first()

    if not found_user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "User deleted successfully"}
