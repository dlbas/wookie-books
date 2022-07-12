from datetime import datetime, timedelta, timezone

from databases.core import Connection
from fastapi import Depends, HTTPException, status
from jose import jwt
from passlib.context import CryptContext

from app.api.deps import (database_connection, token_expires_in_minutes,
                          token_secret_key)
from app.repositories.users import get_user_by_login, update_user_password
from app.schemas.auth import LoginRequest, LoginResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def login_service(
    request: LoginRequest,
    connection: Connection = Depends(database_connection),
    token_expires_in: int = Depends(token_expires_in_minutes),
    secret: str = Depends(token_secret_key),
) -> LoginResponse:
    async with connection:
        await authenticate_user(
            connection, login=request.login, password=request.password
        )
    token = create_token(expires_in=timedelta(minutes=token_expires_in), key=secret)
    return LoginResponse(token=token)


async def authenticate_user(
    connection: Connection, *, login: str, password: str
) -> None:
    user = await get_user_by_login(connection, login=login)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if user.password is None:
        # handle first login
        hashed_password = pwd_context.hash(password)
        await update_user_password(
            connection, user_id=user.id, encrypted_password=hashed_password
        )

    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(*, expires_in: timedelta, key: str) -> str:
    data = {"exp": datetime.now(timezone.utc) + expires_in}
    return jwt.encode(data, key, algorithm="HS256")
