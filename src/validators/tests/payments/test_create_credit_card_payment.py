from src.validators.payments.create_credit_card_payment_validator import create_credit_card_payment_fields
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError
import pytest


def test_valid_request():
    valid_request = {
        'email': 'joao@gmail.com',
        'amount': 100
    }

    create_credit_card_payment_fields(valid_request)


def test_invalid_request():
    invalid_request = {
        'email': 'joao@gmail.com',
        'valor': 100
    }

    with pytest.raises(HttpUnprocessableEntityError):
        create_credit_card_payment_fields(invalid_request)
