from cerberus import Validator
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError


def all_fields_validator(request: any):

    body_validator = Validator({
        'email': {'type': 'string', 'required': True, 'empty': False},
        'senha': {'type': 'string', 'required': True, 'empty': False},
        'saldo': {'type': 'integer', 'required': False, 'empty': False, 'min': 0}
    })

    response = body_validator.validate(request)

    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)
