from databases.core import Connection

from app.models.user import User
from app.repositories.tables.users import users_table


async def get_user_by_login(connection: Connection, *, login: str) -> User | None:
    query = users_table.select(users_table.c.login == login)
    row = await connection.fetch_one(query)
    return User(**dict(row)) if row else None


async def update_user_password(
    connection: Connection, *, user_id: int, encrypted_password: str
) -> None:
    query = users_table.update(users_table.c.id == user_id).values(
        dict(password=encrypted_password)
    )
    await connection.execute(query)
