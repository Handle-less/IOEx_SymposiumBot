from tortoise import Tortoise


async def init_database() -> None:
    await Tortoise.init(
        db_url=f"sqlite://database/db.sqlite",
        modules={
            "models": [
                "database.models.users",
            ],
        },
    )
    await Tortoise.generate_schemas()


async def close_database() -> None:
    await Tortoise.close_connections()
