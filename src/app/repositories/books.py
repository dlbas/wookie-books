from databases.core import Connection

from app.models.book import Book
from app.repositories.tables.books import books_table


async def list_books(connection: Connection) -> list[Book]:
    query = books_table.select()
    rows = await connection.fetch_all(query)
    return [Book(**dict(row)) for row in rows]
