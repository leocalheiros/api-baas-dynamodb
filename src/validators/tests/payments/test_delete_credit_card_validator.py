from src.validators.payments.delete_credit_card_validator import delete_credit_card_fields
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError
import pytest


def test_valid_request():
    valid_request = {
        'email': 'joao@gmail.com'
    }

    delete_credit_card_fields(valid_request)


def test_invalid_request():
    invalid_request = {
        'nome': 'Joao',
        'valor': 100
    }

    with pytest.raises(HttpUnprocessableEntityError):
        delete_credit_card_fields(invalid_request)
