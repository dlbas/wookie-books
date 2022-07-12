from fastapi.routing import APIRoute

from app.schemas.auth import LoginResponse
from app.services.auth import login_service
from app.services.ping import ping_service

routes = [
    # service routes
    APIRoute("/ping/", methods=["GET"], endpoint=ping_service),
    # books routes
    # users routes
    APIRoute(
        "/login/",
        methods=["POST"],
        endpoint=login_service,
        response_model=LoginResponse,
    ),
]
