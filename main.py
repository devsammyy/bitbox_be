from typing import Annotated, Union
from fastapi import FastAPI, Depends
from modules.db.database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from modules.models import user


app = FastAPI()
user.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/{item_id}")
async def root(item_id: int, q: Union[int, str, bool] = None):
    return {"message": f" item_id: {item_id}, some query: {q}"}
