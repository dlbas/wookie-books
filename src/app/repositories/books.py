from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from databases.core import Connection
from sqlalchemy import insert, select, update

from app.models.book import Book
from app.repositories.tables.books import books_table
from app.repositories.tables.users import users_table


async def list_books(connection: Connection) -> list[Book]:
    query = (
        select(
            [
                books_table.c.id,
                books_table.c.title,
                books_table.c.description,
                books_table.c.cover_image_url,
                books_table.c.price,
                users_table.c.pseudonym.label("author_pseudonym"),
            ]
        )
        .select_from(books_table.join(users_table))
        .where(books_table.c.unpublished_at.is_(None))
    )
    rows = await connection.fetch_all(query)
    return [Book(**dict(row)) for row in rows]


async def get_book_by_id(
    connection: Connection, *, book_id: int, author_id: int = None
) -> Book | None:
    query = (
        select(
            [
                books_table.c.id,
                books_table.c.title,
                books_table.c.description,
                books_table.c.cover_image_url,
                books_table.c.price,
                users_table.c.pseudonym.label("author_pseudonym"),
            ]
        )
        .select_from(books_table.join(users_table))
        .where(
            books_table.c.id == book_id,
        )
    )
    if author_id is not None:
        query = query.where(
            books_table.c.user_id == author_id, books_table.c.unpublished_at.is_(None)
        )

    row = await connection.fetch_one(query)
    return Book(**dict(row)) if row else None


async def create_book(
    connection: Connection,
    *,
    title: str,
    description: str,
    author_id: int,
    cover_image_url: str,
    price: Decimal,
) -> None:
    query = insert(books_table).values(
        title=title,
        description=description,
        user_id=author_id,
        cover_image_url=cover_image_url,
        price=price,
    )

    await connection.execute(query)


async def update_book(
    connection: Connection, *, book_id: int, values: dict[str, Any]
) -> None:
    query = (
        update(
            books_table,
        )
        .where(
            books_table.c.id == book_id,
        )
        .values(values)
    )

    await connection.execute(query)


async def unpublish_book(connection: Connection, *, book_id: int) -> None:
    query = (
        update(books_table)
        .where(books_table.c.id == book_id)
        .values(unpublished_at=datetime.now(timezone.utc))
    )

    await connection.execute(query)
