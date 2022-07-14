import pytest
from fastapi.testclient import TestClient

from app.api.database import database_connection
from app.main import app


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


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
