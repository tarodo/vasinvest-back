import secrets
from decouple import config

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM: str = 'HS256'
    DATABASE_URL: str = 'sqlite://db.sqlite3'

    FIRST_SUPERUSER: EmailStr = config("ADMIN_EMAIL")
    FIRST_SUPERUSER_PASSWORD: str = config("ADMIN_PSWD")

    TEST_USER_EMAIL: EmailStr = "test@example.com"
    TEST_USER_PASS: str = 'secret_password'


settings = Settings()
