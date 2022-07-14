from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from app.api.database import database_connection
from app.api.deps import token_secret_key
from app.main import app
from app.services.auth import JWT_ALG


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def auth_header() -> str:
    key = "test"
    app.dependency_overrides[token_secret_key] = lambda: key
    payload = {"exp": datetime.now(timezone.utc) + timedelta(minutes=60), "sub": "test"}
    encoded = jwt.encode(payload, key=key, algorithm=JWT_ALG)
    yield "Bearer " + encoded
    del app.dependency_overrides[token_secret_key]


@pytest.fixture
def test_connection(mocker):
    connection = mocker.AsyncMock()

    async def aenter(self):
        ...

    async def aexit(self, exc_type, exc, tb):
        if exc:
            raise exc

    connection.__aenter__ = aenter
    connection.__aexit__ = aexit

    app.dependency_overrides[database_connection] = lambda: connection
    yield connection
    del app.dependency_overrides[database_connection]
