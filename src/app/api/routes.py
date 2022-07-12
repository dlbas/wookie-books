from fastapi.routing import APIRoute

from app.schemas.auth import LoginResponse
from app.services.auth import login_service
from app.services.books import list_books
from app.services.ping import ping_service

routes = [
    # service routes
    APIRoute("/ping/", methods=["GET"], endpoint=ping_service),
    # books routes
    APIRoute(
        "/books/",
        methods=["GET"],
        endpoint=list_books,
    ),
    # users routes
    APIRoute(
        "/login/",
        methods=["POST"],
        endpoint=login_service,
        response_model=LoginResponse,
    ),
]
