from fastapi import FastAPI, Depends
from modules.db.database import Base, engine, SessionLocal
from modules.db import database
from modules.router import user_router


app = FastAPI(

    title="Bitbox API",
    description="An API to manage church activities",
    version="0.1.0"
)


database.Base.metadata.create_all(bind=engine)


app.include_router(user_router.router, prefix="/api/v1", tags=["Users"])
