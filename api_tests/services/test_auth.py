from fastapi import HTTPException, status


def test_login_service__authenticates_active_user(test_connection, test_client, mocker):
    mocker.patch("app.services.auth.authenticate_user")
    response = test_client.post(
        "/login/", data={"username": "test", "password": "test"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"access_token": mocker.ANY, "token_type": "bearer"}


def test_login_service__errors_when_cannot_authenticate_user(
    test_connection, test_client, mocker
):
    mocker.patch(
        "app.services.auth.authenticate_user",
        side_effect=HTTPException(status_code=status.HTTP_403_FORBIDDEN),
    )
    response = test_client.post(
        "/login/", data={"username": "test", "password": "test"}
    )

    assert response.status_code != status.HTTP_200_OK
