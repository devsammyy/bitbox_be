from fastapi import FastAPI, Depends
import os
import uvicorn
from modules.auth import auth_router
from modules.db.database import Base
from fastapi.middleware.cors import CORSMiddleware
from modules.user import user_router


app = FastAPI(

    title="Bitbox API",
    description="An API to manage church activities",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Base.metadata.create_all(bind=engine)


app.include_router(user_router.router, prefix="/api/v1", tags=["Users"])
app.include_router(auth_router.router, prefix="/api/v1", tags=["Auth"])


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
