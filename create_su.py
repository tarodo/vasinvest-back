from tortoise import Tortoise, run_async

from app.core.config import settings
from app.crud.users import create, get_by_email
from app.models import Users
from app.schemas.users import UserIn


async def admin_creator(db: str, email: str, password: str) -> None:
    await Tortoise.init(
        db_url=db,
        modules={"models": ["app.models.users"]},
    )
    admin: Users = await get_by_email(email)
    if admin:
        print(f"Admin ID : {admin.id}")
        return None

    admin_in = UserIn(email=email, password=password, is_superuser=True, is_active=True)
    admin = await create(admin_in)
    print(f"Mission complete. Admin with ID : {admin.id}")


async def user_creator(db: str, email: str, password: str) -> None:
    await Tortoise.init(
        db_url=db,
        modules={"models": ["app.models.users"]},
    )
    user: Users = await get_by_email(email)
    if user:
        print(f"Test User ID : {user.id}")
        return None

    admin_in = UserIn(
        email=email, password=password, is_superuser=False, is_active=True
    )
    admin = await create(admin_in)
    print(f"Mission complete. Test User with ID : {admin.id}")


if __name__ == "__main__":
    run_async(
        admin_creator(
            settings.DATABASE_URL,
            settings.FIRST_SUPERUSER,
            settings.FIRST_SUPERUSER_PASSWORD,
        )
    )

    run_async(
        user_creator(
            settings.DATABASE_URL, settings.TEST_USER_EMAIL, settings.TEST_USER_PASS
        )
    )
