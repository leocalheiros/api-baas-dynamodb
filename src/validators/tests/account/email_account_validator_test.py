from src.validators.account.email_account_validator import email_field_validator
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError
import pytest


def test_valid_request():
    valid_request = {
        'email': 'joão@gmail.com',
    }

    email_field_validator(valid_request)


def test_invalid_request():
    invalid_request = {
        'saldo': 123
    }

    with pytest.raises(HttpUnprocessableEntityError):
        email_field_validator(invalid_request)
