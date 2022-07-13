from datetime import datetime, timedelta, timezone

from databases.core import Connection
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

from app.api.database import database_connection
from app.api.deps import (oauth2_scheme, token_expires_in_minutes,
                          token_secret_key)
from app.models.user import User
from app.repositories.users import get_user_by_login, update_user_password
from app.schemas.auth import LoginResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_ALG = "HS256"


async def login_service(
    request: OAuth2PasswordRequestForm = Depends(),
    connection: Connection = Depends(database_connection),
    token_expires_in: int = Depends(token_expires_in_minutes),
    secret: str = Depends(token_secret_key),
) -> LoginResponse:
    """Login endpoint"""
    async with connection:
        await authenticate_user(
            connection, login=request.username, password=request.password
        )
    token = create_token(
        expires_in=timedelta(minutes=token_expires_in),
        username=request.username,
        key=secret,
    )
    return LoginResponse(access_token=token)


async def authenticate_user(
    connection: Connection, *, login: str, password: str
) -> None:
    """Authenticates user by login and password"""
    user = await get_user_by_login(connection, login=login)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if user.password is None:
        # handle first login
        hashed_password = pwd_context.hash(password)
        await update_user_password(
            connection, user_id=user.id, encrypted_password=hashed_password
        )
        return

    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    secret: str = Depends(token_secret_key),
    connection: Connection = Depends(database_connection),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret, [JWT_ALG])
    except jwt.JWTError:
        raise credentials_exception

    login = payload.get("sub")
    if login is None:
        raise credentials_exception

    async with connection:
        user = await get_user_by_login(connection, login=login)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(*, expires_in: timedelta, username: str, key: str) -> str:
    data = {"exp": datetime.now(timezone.utc) + expires_in, "sub": username}
    return jwt.encode(data, key, algorithm=JWT_ALG)
