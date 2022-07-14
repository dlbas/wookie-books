import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.database import database_connection


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)

@pytest.fixture
def test_connection(mocker):
    connection = mocker.Mock()
    app.dependency_overrides[database_connection] = lambda: connection
    yield connection
    # del app.dependency_overrides[database_connection]
