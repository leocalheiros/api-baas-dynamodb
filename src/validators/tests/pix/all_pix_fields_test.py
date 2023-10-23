from src.validators.pix.all_pix_fields_validator import all_pix_fields
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError
import pytest


def test_valid_request():
    valid_request = {
        'nome': 'João Silva',
        'chavepix': "+5544998309823",
        'valor': '100.00',
        'cidade': 'Maringá'
    }

    all_pix_fields(valid_request)


def test_invalid_request():
    invalid_request = {
        'nome': 'Maria',
        'valor': '0'
    }

    with pytest.raises(HttpUnprocessableEntityError):
        all_pix_fields(invalid_request)
