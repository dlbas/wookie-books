from sqlalchemy import (DECIMAL, TIMESTAMP, Column, ForeignKey, Integer,
                        String, Table)

from .metadata import metadata
from .users import users_table

books_table = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("description", String, nullable=False),
    Column("cover_image_url", String, nullable=False),
    Column("price", DECIMAL, nullable=False),
    Column("unpublished_at", TIMESTAMP(timezone=True), nullable=False),
    Column("user_id", ForeignKey(users_table.c.id)),
)
