from src.validators.account.email_and_senha_validator import email_and_senha_validator
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError
import pytest


def test_valid_request():
    valid_request = {
        'email': 'joão@gmail.com',
        'senha': '123'
    }

    email_and_senha_validator(valid_request)


def test_invalid_request():
    invalid_request = {
        'email': 'leo@gmail.com'
    }

    with pytest.raises(HttpUnprocessableEntityError):
        email_and_senha_validator(invalid_request)
