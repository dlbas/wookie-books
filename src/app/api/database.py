from databases import Database

database = Database("sqlite+aiosqlite://./example.db")


async def database_connection():
    return database.connection()
