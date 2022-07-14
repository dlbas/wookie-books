from fastapi import status


def test_list_books__allows_listing_without_auth(test_client, test_connection):
    test_connection.fetch_all.return_value = []
    response = test_client.get("/books/")

    assert response.status_code == status.HTTP_200_OK
    assert test_connection.fetch_all.called
    assert response.json() == []


def test_list_books__allows_detail_without_auth(test_client, test_connection):
    test_connection.fetch_one.return_value = None
    response = test_client.get("/books/1/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert test_connection.fetch_one.called
