from tortoise import Tortoise, run_async

from app.crud.users import create
from app.schemas.users import UserIn

from app.core.config import settings


async def admin_creator(db: str, email: str, password: str) -> None:
    await Tortoise.init(
        db_url=db,
        modules={"models": ["app.models.users"]},
    )
    admin_in = UserIn(email=email, password=password, is_superuser=True, is_active=True)
    admin = await create(admin_in)
    print(f"Mission complete. Admin with ID : {admin.id}")


if __name__ == "__main__":
    run_async(
        admin_creator(
            settings.DATABASE_URL, settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD
        )
    )
