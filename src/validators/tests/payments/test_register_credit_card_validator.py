from src.validators.payments.register_credit_card_validator import register_credit_card_fields
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError
import pytest


def test_valid_request():
    valid_request = {
        'email': 'joao@gmail.com',
        'card_number': "4134185779995000",
        'expiration_month': 9,
        'expiration_year': 2025,
        'security_code': '191',
        'holder_name': 'Julio Alvarenga'
    }

    register_credit_card_fields(valid_request)


def test_invalid_request():
    invalid_request = {
        'email': 'joao@gmail.com',
        'expiration_month': 9,
        'expiration_year': 2025,
        'security_code': '191',
        'holder_name': 'Julio Alvarenga'
    }

    with pytest.raises(HttpUnprocessableEntityError):
        register_credit_card_fields(invalid_request)


# 'email': {'type': 'string', 'required': True, 'empty': False},
#         'card_number': {'type': 'string', 'required': True, 'empty': False},
#         'expiration_month': {'type': 'integer', 'required': True, 'empty': False},
#         'expiration_year': {'type': 'integer', 'required': True, 'empty': False},
#         'security_code': {'type': 'string', 'required': False, 'empty': False},
#         'holder_name': {'type': 'string', 'required': True, 'empty': False}