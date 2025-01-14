from fastapi import FastAPI, Depends
from modules.auth import auth_router
from modules.db.database import Base, engine

from modules.user import user_router


app = FastAPI(

    title="Bitbox API",
    description="An API to manage church activities",
    version="0.1.0"
)


Base.metadata.create_all(bind=engine)


app.include_router(user_router.router, prefix="/api/v1", tags=["Users"])
app.include_router(auth_router.router, prefix="/api/v1", tags=["Auth"])
