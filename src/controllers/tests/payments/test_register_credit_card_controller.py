import pytest
from unittest.mock import Mock
from src.controllers.payments.register_credit_card_controller import RegisterCardController
from src.models.interface.account_interface import AccountRepositoryInterface
from src.models.interface.credit_card_interface import CreditCardRepositoryInterface
from src.errors.types.http_unauthorized import HttpUnauthorizedError
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_bad_request import HttpBadRequest



def create_account_model_mock(exists=True):
    account_model_mock = Mock(spec=AccountRepositoryInterface)
    account_model_mock.check_account_exists.return_value = exists
    return account_model_mock


def create_card_model_mock():
    return Mock(spec=CreditCardRepositoryInterface)


def test_register_card_controller_success():
    account_model_mock = create_account_model_mock(exists=True)
    card_model_mock = create_card_model_mock()
    controller = RegisterCardController(account_model_mock, card_model_mock)

    request_data = {
        'email': 'user@example.com',
        'card_number': '4111111111111111',
        'expiration_month': 12,
        'expiration_year': 2025,
        'security_code': '123',
        'holder_name': 'John Doe',
    }

    response = controller.operate(request_data, 'user@example.com')

    assert response == {
        "data": {
            "status": "success",
            "email": 'user@example.com'
        }
    }

def test_register_card_controller_account_not_found():
    account_model_mock = create_account_model_mock(exists=False)
    card_model_mock = create_card_model_mock()
    controller = RegisterCardController(account_model_mock, card_model_mock)

    request_data = {
        'email': 'user@example.com',
        'card_number': '4111111111111111',
        'expiration_month': 12,
        'expiration_year': 2025,
        'security_code': '123',
        'holder_name': 'John Doe',
    }

    with pytest.raises(HttpNotFoundError):
        controller.operate(request_data, 'user@example.com')



def test_register_card_controller_invalid_card_number():
    account_model_mock = create_account_model_mock(exists=True)
    card_model_mock = create_card_model_mock()
    controller = RegisterCardController(account_model_mock, card_model_mock)

    request_data = {
        'email': 'user@example.com',
        'card_number': '1234567890123456',  # Número inválido
        'expiration_month': 12,
        'expiration_year': 2025,
        'security_code': '123',
        'holder_name': 'John Doe',
    }

    with pytest.raises(HttpBadRequest):
        controller.operate(request_data, 'user@example.com')
