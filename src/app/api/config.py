from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite://./example.db"

    token_secret_key: str = "replace me"
    token_expires_in_minutes: int = 60
