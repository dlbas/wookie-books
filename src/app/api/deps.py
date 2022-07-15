from fastapi.security import OAuth2PasswordBearer

from app.api.config import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


def token_secret_key() -> str:
    return Settings().token_secret_key


def token_expires_in_minutes() -> int:
    return Settings().token_expires_in_minutes
