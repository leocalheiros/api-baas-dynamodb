from cerberus import Validator
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError


def all_fields_validator(request: any):

    body_validator = Validator({
        'source_email': {'type': 'string', 'required': True, 'empty': False},
        'target_email': {'type': 'string', 'required': True, 'empty': False},
        'amount': {'type': 'integer', 'required': True, 'empty': False, 'min': 1},
    })

    response = body_validator.validate(request)

    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)
