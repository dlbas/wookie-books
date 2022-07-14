import pytest
from fastapi import HTTPException, status

from app.services.auth import authenticate_user, get_current_user


@pytest.mark.anyio
async def test_authenticate_user__raises_when_cannot_find_user(mocker):
    mocker.patch("app.services.auth.get_user_by_login", return_value=None)

    with pytest.raises(HTTPException):
        await authenticate_user(mocker.Mock(), login="test", password="test")


@pytest.mark.anyio
async def test_authenticate_user__raises_when_found_user_is_not_active(mocker):
    mocker.patch(
        "app.services.auth.get_user_by_login", return_value=mocker.Mock(is_active=False)
    )

    with pytest.raises(HTTPException):
        await authenticate_user(mocker.Mock(), login="test", password="test")


@pytest.mark.anyio
async def test_authenticate_user__updates_password_when_none(mocker):
    mocker.patch(
        "app.services.auth.get_user_by_login",
        return_value=mocker.Mock(is_active=True, password=None, id=1),
    )
    update_password_mock = mocker.patch("app.services.auth.update_user_password")

    await authenticate_user(mocker.Mock(), login="test", password="test")

    update_password_mock.assert_called_once_with(
        mocker.ANY, user_id=1, encrypted_password=mocker.ANY
    )


@pytest.mark.anyio
async def test_authenticate_user__raises_when_passwords_do_not_match(mocker):
    mocker.patch(
        "app.services.auth.get_user_by_login",
        return_value=mocker.Mock(
            is_active=True,
            password="$2b$12$xnVAmuXHuVEavUS8RcCA3O/Ney8saw15mj03Gzh90DRy7ZSchRko.",
            id=1,
        ),
    )

    with pytest.raises(HTTPException):
        await authenticate_user(mocker.Mock(), login="test", password="qwerty")


@pytest.mark.anyio
async def test_get_current_user__raises_when_jwt_decode_failed(mocker):
    with pytest.raises(HTTPException):
        await get_current_user(token="test", secret="test", connection=mocker.Mock())


@pytest.mark.anyio
async def test_get_current_user__raises_when_no_such_user(mocker, jwt_token):
    mocker.patch("app.services.auth.get_user_by_login", return_value=None)
    token, secret = jwt_token
    with pytest.raises(HTTPException):
        await get_current_user(
            token=token, secret=secret, connection=mocker.MagicMock()
        )


@pytest.mark.anyio
async def test_get_current_user__raises_when_user_is_no_active(mocker, jwt_token):
    mocker.patch(
        "app.services.auth.get_user_by_login", return_value=mocker.Mock(is_active=False)
    )
    token, secret = jwt_token
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(
            token=token, secret=secret, connection=mocker.MagicMock()
        )
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
