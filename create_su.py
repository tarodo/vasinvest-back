from decouple import config
from tortoise import Tortoise, run_async

from app.crud.users import create
from app.schemas.users import UserIn

EMAIL_DEFAULT = "test@mo.ru"
PASS_DEFAULT = "PassPa$$001"


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
            config("DATABASE_URL"), config("ADMIN_EMAIL"), config("ADMIN_PSWD")
        )
    )
