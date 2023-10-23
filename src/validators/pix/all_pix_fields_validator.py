from cerberus import Validator
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError


def all_pix_fields(request: any):

    body_validator = Validator({
        'nome': {'type': 'string', 'required': True, 'empty': False},
        'chavepix': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 32},
        'valor': {'type': 'string', 'required': True, 'empty': False, 'minlength': 4},
        'cidade': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 32},
        'txtId': {'type': 'string', 'required': False, 'empty': False, 'maxlength': 72},
    })

    response = body_validator.validate(request)

    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)
