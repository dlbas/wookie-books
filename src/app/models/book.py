from pydantic import BaseModel


class Book(BaseModel):
    title: str
    description: str
    author_id: int
