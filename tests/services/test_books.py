from app.main import app
from app.api.database import database_connection


def test_list_books__allows_listing_without_auth(test_client, test_connection, mocker):
    app.dependency_overrides[database_connection] = lambda: mocker.Mock()
    response = test_client.request('GET', '/books/')