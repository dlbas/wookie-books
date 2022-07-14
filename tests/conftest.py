from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt


@pytest.fixture
def jwt_token():
    secret = "test"
    payload = {"sub": "test", "exp": datetime.now(timezone.utc) + timedelta(minutes=60)}
    return jwt.encode(payload, key=secret), secret
