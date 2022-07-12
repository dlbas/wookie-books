from fastapi import FastAPI

from app.api.config import Settings
from app.api.database import database_container
from app.api.routes import routes

app = FastAPI(routes=routes)


@app.on_event("startup")
async def connect_to_database():
    db_url = Settings().database_url
    database_container.setup(db_url)
    await database_container.connect()


@app.on_event("shutdown")
async def disconnect_from_database():
    await database_container.disconnect()
