from fastapi import FastAPI

from app.api import users
from db import init_db


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(users.router, tags=["users"])

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
