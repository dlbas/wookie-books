from decimal import Decimal

from pydantic import BaseModel


class BookForGet(BaseModel):
    id: int
    title: str
    description: str
    cover_image_url: str
    price: Decimal
    author_pseudonym: str


class BookForCreate(BaseModel):
    title: str
    description: str
    cover_image_url: str
    price: Decimal


class BookForUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    cover_image_url: str | None = None
    price: Decimal | None = None
