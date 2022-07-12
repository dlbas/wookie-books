from databases import Database
from databases.core import Connection


class DatabaseContainer:
    def __init__(self):
        self.database: Database | None = None

    async def connect(self):
        await self.database.connect()

    async def disconnect(self):
        await self.database.disconnect()

    def connection(self) -> Connection:
        return self.database.connection()

    def setup(self, url: str):
        self.database = Database(url)


database_container = DatabaseContainer()


async def database_connection():
    return database_container.connection()
