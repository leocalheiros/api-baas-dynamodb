from cerberus import Validator
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError


def register_credit_card_fields(request: any):

    body_validator = Validator({
        'email': {'type': 'string', 'required': True, 'empty': False},
        'card_number': {'type': 'string', 'required': True, 'empty': False},
        'expiration_month': {'type': 'integer', 'required': True, 'empty': False},
        'expiration_year': {'type': 'integer', 'required': True, 'empty': False},
        'security_code': {'type': 'string', 'required': False, 'empty': False},
        'holder_name': {'type': 'string', 'required': True, 'empty': False}
    })

    response = body_validator.validate(request)

    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)
