from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.api.config import Settings
from app.api.database import database_connection
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return User(id=1, login="test", password="test", pseudonym="test", is_active=True)


def token_secret_key() -> str:
    return Settings().token_secret_key


def token_expires_in_minutes() -> int:
    return Settings().token_expires_in_minutes
