from sqlalchemy import Boolean, Column, Integer, String, Table

from .metadata import metadata

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String, nullable=False),
    Column("password", String, nullable=False),
    Column("pseudonym", String, nullable=True),
    Column("is_active", Boolean, nullable=False),
)
