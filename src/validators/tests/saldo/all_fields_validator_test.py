from src.validators.saldo.all_fields_validator import all_fields_validator
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError
import pytest


def test_valid_request():
    valid_request = {
        'source_email': 'joão@gmail.com',
        'target_email': 'leo@gmail.com',
        'amount': 100
    }

    all_fields_validator(valid_request)


def test_invalid_request():
    invalid_request = {
        'target_email': 'leo@gmail.com',
        'amount': 5
    }

    with pytest.raises(HttpUnprocessableEntityError):
        all_fields_validator(invalid_request)


def test_negative_saldo():
    invalid_request={
        'source_email': 'joao@gmail.com',
        'traget_email': 'leo@gmail.com',
        'saldo': -1
    }

    with pytest.raises(HttpUnprocessableEntityError):
        all_fields_validator(invalid_request)


def test_not_min_saldo():
    invalid_request = {
        'source_email': 'joao@gmail.com',
        'traget_email': 'leo@gmail.com',
        'saldo': 0
    }

    with pytest.raises(HttpUnprocessableEntityError):
        all_fields_validator(invalid_request)
