from decouple import config
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

TORTOISE_ORM = {
    "connections": {"default": config("DATABASE_URL")},
    "apps": {
        "models": {
            "models": [
                "app.models.users",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=config("DATABASE_URL"),
        modules={
            "models": [
                "app.models.users",
            ]
        },
        generate_schemas=True,
        add_exception_handlers=True,
    )
