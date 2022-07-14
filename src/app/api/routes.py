import fastapi
from fastapi.routing import APIRoute

from app.schemas.auth import LoginResponse
from app.schemas.books import BookForGet
from app.services.auth import login_service
from app.services.books import (create_book, delete_book, get_book_by_id,
                                list_books, update_book)
from app.services.ping import ping_service

routes = [
    # service routes
    APIRoute("/ping/", methods=["GET"], endpoint=ping_service, tags=["service"]),
    # books routes
    APIRoute(
        "/books/",
        methods=["GET"],
        endpoint=list_books,
        tags=["books"],
        response_model=list[BookForGet],
    ),
    APIRoute(
        "/books/{book_id}/",
        methods=["GET"],
        endpoint=get_book_by_id,
        tags=["books"],
        response_model=BookForGet,
    ),
    APIRoute("/books/", methods=["POST"], endpoint=create_book, tags=["books"]),
    APIRoute(
        "/books/{book_id}/", methods=["PUT"], endpoint=update_book, tags=["books"]
    ),
    APIRoute(
        "/books/{book_id}/", methods=["DELETE"], endpoint=delete_book, tags=["books"]
    ),
    # users routes
    APIRoute(
        "/login/",
        methods=["POST"],
        endpoint=login_service,
        response_model=LoginResponse,
        tags=["login"],
    ),
]

router = fastapi.APIRouter(routes=routes)
