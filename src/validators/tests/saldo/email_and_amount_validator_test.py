from src.validators.saldo.email_and_amount_validator import email_and_amount_validator
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError
import pytest


def test_valid_request():
    valid_request = {
        'email': 'joão@gmail.com',
        'amount': 100
    }

    email_and_amount_validator(valid_request)


def test_invalid_request():
    invalid_request = {
        'target_email': 'leo@gmail.com',
        'amount': 5
    }

    with pytest.raises(HttpUnprocessableEntityError):
        email_and_amount_validator(invalid_request)


def test_not_min_saldo():
    invalid_request={
        'email': 'joao@gmail.com',
        'saldo': 0
    }

    with pytest.raises(HttpUnprocessableEntityError):
        email_and_amount_validator(invalid_request)
