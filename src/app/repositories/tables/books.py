from sqlalchemy import Column, ForeignKey, Integer, String, Table

from .metadata import metadata
from .users import users_table

books_table = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("description", String, nullable=False),
    Column("user_id", ForeignKey(users_table.c.id)),
)
