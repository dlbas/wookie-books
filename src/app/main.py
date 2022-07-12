from fastapi import FastAPI

from app.api.database import database
from app.api.routes import routes

app = FastAPI(routes=routes)


@app.on_event("startup")
async def connect_to_database():
    await database.connect()


@app.on_event("shutdown")
async def disconnect_from_database():
    await database.disconnect()
