from pydantic import BaseSettings


class Settings(BaseSettings):
    token_secret_key: str = "replace me"
    token_expires_in_minutes: int = 60
