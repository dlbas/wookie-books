from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    description: str
    cover_image_url: str
    price: Decimal
    author_pseudonym: str
    unpublished_at: datetime | None = None
