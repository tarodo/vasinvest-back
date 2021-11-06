from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import currencies, login, platforms, tickers, users
from db import init_db


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(login.router, tags=["login"])
    application.include_router(users.router, prefix="/users", tags=["users"])
    application.include_router(
        platforms.router, prefix="/platforms", tags=["platforms"]
    )
    application.include_router(tickers.router, prefix="/tickers", tags=["tickers"])
    application.include_router(
        currencies.router, prefix="/currencies", tags=["currencies"]
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "DELETE"],
        allow_headers=["*"],
    )

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
