from fastapi import status

from app.models.user import User


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


def test_create_book__unauthorized_user_cannot_create_book(
    test_client, test_connection
):
    response = test_client.post(
        "/books/",
        json={
            "title": "test",
            "description": "test",
            "price": 1,
            "cover_image_url": "https://example.com",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not test_connection.fetch_one.called


def test_create_book__disabled_user_cannot_create_book(
    test_client, test_connection, auth_header, mocker
):
    mocker.patch(
        "app.services.auth.get_user_by_login",
        return_value=User(
            id=1, login="test", password=None, pseudonym="test", is_active=False
        ),
    )
    response = test_client.post(
        "/books/",
        json={
            "title": "test",
            "description": "test",
            "price": 1,
            "cover_image_url": "https://example.com",
        },
        headers={"Authorization": auth_header},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_book__disabled_user_cannot_update_book(
    test_client, test_connection, auth_header, mocker
):
    mocker.patch(
        "app.services.auth.get_user_by_login",
        return_value=User(
            id=1, login="test", password=None, pseudonym="test", is_active=False
        ),
    )
    response = test_client.put(
        "/books/1/",
        json={
            "title": "test",
            "description": "test",
            "price": 1,
            "cover_image_url": "https://example.com",
        },
        headers={"Authorization": auth_header},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_book__disabled_user_cannot_delete_book(
    test_client, test_connection, auth_header, mocker
):
    mocker.patch(
        "app.services.auth.get_user_by_login",
        return_value=User(
            id=1, login="test", password=None, pseudonym="test", is_active=False
        ),
    )
    response = test_client.delete(
        "/books/1/",
        headers={"Authorization": auth_header},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_book__user_cannot_delete_book_of_another_user(
    test_client, test_connection, auth_header, mocker
):
    mocker.patch(
        "app.services.auth.get_user_by_login",
        return_value=User(
            id=1, login="test", password=None, pseudonym="test", is_active=True
        ),
    )
    mocker.patch(
        "app.services.books.get_book_by_id_db",
        return_value=None,  # cannot find book by this user id in db
    )
    response = test_client.delete(
        "/books/1/",
        headers={"Authorization": auth_header},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
