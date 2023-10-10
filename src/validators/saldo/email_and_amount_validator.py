from cerberus import Validator
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError


def email_and_amount_validator(request: any):

    body_validator = Validator({
        'email': {'type': 'string', 'required': True, 'empty': False},
        'amount': {'type': 'integer', 'required': True, 'empty': False, 'min': 1},
    })

    response = body_validator.validate(request)

    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)
