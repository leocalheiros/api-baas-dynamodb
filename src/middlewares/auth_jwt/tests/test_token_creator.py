import pytest
from src.middlewares.auth_jwt.token_creator import TokenCreator


@pytest.fixture
def token_creator():
    token_key = "secret_key"
    exp_time_min = 15
    refresh_time_min = 10
    return TokenCreator(token_key, exp_time_min, refresh_time_min)


def test_create_token(token_creator):
    email = "test@example.com"
    token = token_creator.create(email)

    assert isinstance(token, str)
    assert token


def test_encode_token(token_creator):
    email = "test@example.com"
    token = token_creator._TokenCreator__encode_token(email)
    assert isinstance(token, str)
    assert token
