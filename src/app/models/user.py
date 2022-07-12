from pydantic import BaseModel


class User(BaseModel):
    id: int
    login: str
    password: str | None
    pseudonym: str
    is_active: bool
