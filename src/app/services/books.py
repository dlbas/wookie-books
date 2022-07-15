from databases.core import Connection
from fastapi import Depends, HTTPException, Path, Response, status

from app.api.database import database_connection
from app.models.user import User
from app.repositories.books import create_book as create_book_db
from app.repositories.books import get_book_by_id as get_book_by_id_db
from app.repositories.books import list_books as list_books_db
from app.repositories.books import unpublish_book as unpublish_book_db
from app.repositories.books import update_book as update_book_db
from app.schemas.books import BookForCreate, BookForGet, BookForUpdate
from app.services.auth import get_current_user


async def list_books(
    connection: Connection = Depends(database_connection),
) -> list[BookForGet]:
    async with connection:
        books = await list_books_db(connection)
    return [BookForGet(**book.dict()) for book in books]


async def get_book_by_id(
    book_id: int = Path(),
    connection: Connection = Depends(database_connection),
) -> BookForGet:
    async with connection:
        book = await get_book_by_id_db(connection, book_id=book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return BookForGet(**book.dict())


async def create_book(
    book: BookForCreate,
    user: User = Depends(get_current_user),
    connection: Connection = Depends(database_connection),
):
    async with connection:
        await create_book_db(
            connection,
            title=book.title,
            description=book.description,
            author_id=user.id,
            cover_image_url=book.cover_image_url,
            price=book.price,
        )
    return Response(status_code=status.HTTP_201_CREATED)


async def update_book(
    update: BookForUpdate,
    book_id: int = Path(),
    user: User = Depends(get_current_user),
    connection: Connection = Depends(database_connection),
):
    updates = update.dict(exclude_unset=True)
    async with connection:
        book = await get_book_by_id_db(connection, book_id=book_id, author_id=user.id)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        await update_book_db(connection, book_id=book.id, values=updates)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def delete_book(
    book_id: int = Path(),
    connection: Connection = Depends(database_connection),
    user: User = Depends(get_current_user),
):
    async with connection:
        book = await get_book_by_id_db(connection, book_id=book_id, author_id=user.id)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        await unpublish_book_db(connection, book_id=book.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
