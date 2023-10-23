from src.validators.account.create_account_validator import all_fields_validator
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError
import pytest


def test_valid_request():
    valid_request = {
        'email': 'joão@gmail.com',
        'senha': "123",
        'saldo': 100
    }

    all_fields_validator(valid_request)


def test_invalid_request():
    invalid_request = {
        'email': 'leo@gmail.com',
        'valor': '5'
    }

    with pytest.raises(HttpUnprocessableEntityError):
        all_fields_validator(invalid_request)


def test_negative_saldo():
    invalid_request = {
        'email': 'leo@gmail.com',
        'senha': '123',
        'saldo': -1
    }

    with pytest.raises(HttpUnprocessableEntityError):
        all_fields_validator(invalid_request)


def test_without_saldo():
    valid_request = {
        'email': 'leo@gmail.com',
        'senha': '123'
    }

    # must be success, because saldo is not required = True
    all_fields_validator(valid_request)
