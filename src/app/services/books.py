from databases.core import Connection
from fastapi import Depends

from app.api.database import database_connection
from app.models.book import Book
from app.repositories.books import list_books as list_books_db


async def list_books(
    connection: Connection = Depends(database_connection),
) -> list[Book]:
    async with connection:
        books = await list_books_db(connection)
    return books
