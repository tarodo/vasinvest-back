from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models.users",
                "aerich.models",
                "app.models.platforms",
                "app.models.tickers",
                "app.models.currencies",
            ],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={
            "models": [
                "app.models.users",
                "app.models.platforms",
                "app.models.tickers",
                "app.models.currencies",
            ]
        },
        generate_schemas=True,
        add_exception_handlers=True,
    )
