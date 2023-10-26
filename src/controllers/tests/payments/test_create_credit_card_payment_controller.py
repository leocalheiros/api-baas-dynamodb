import pytest
from unittest.mock import Mock
from src.controllers.payments.create_credit_card_payment_controller import TransactionController
from src.models.interface.account_interface import AccountRepositoryInterface
from src.models.interface.credit_card_interface import CreditCardRepositoryInterface
from src.errors.types.http_not_found import HttpNotFoundError


def create_account_model_mock(exists=True):
    account_model_mock = Mock(spec=AccountRepositoryInterface)
    account_model_mock.check_account_exists.return_value = exists
    return account_model_mock


def create_card_model_mock(has_credit_card=True):
    card_model_mock = Mock(spec=CreditCardRepositoryInterface)
    if has_credit_card:
        card_model_mock.get_credit_card.return_value = {
            "card_number": "NDEzNDE4NTc3OTk5NTAwMA=="
        }
    else:
        card_model_mock.get_credit_card.return_value = None
    return card_model_mock


def test_transaction_controller_success():
    account_model_mock = create_account_model_mock(exists=True)
    card_model_mock = create_card_model_mock(has_credit_card=True)
    controller = TransactionController(account_model_mock, card_model_mock)

    request_data = {
        'email': 'user@example.com',
        'amount': 100.0,
    }

    response = controller.operate(request_data, 'user@example.com')

    expected_response = {
        "status": "success",
        "email": 'user@example.com',
        "amount": 100.0,
        "card_number": "4134185779995000"
    }

    assert response == expected_response


def test_transaction_controller_account_not_found():
    account_model_mock = create_account_model_mock(exists=False)
    card_model_mock = create_card_model_mock(has_credit_card=True)
    controller = TransactionController(account_model_mock, card_model_mock)

    request_data = {
        'email': 'user@example.com',
        'amount': 100.0,
    }

    with pytest.raises(HttpNotFoundError):
        controller.operate(request_data, 'user@example.com')


def test_transaction_controller_no_credit_card():
    account_model_mock = create_account_model_mock(exists=True)
    card_model_mock = create_card_model_mock(has_credit_card=False)
    controller = TransactionController(account_model_mock, card_model_mock)

    request_data = {
        'email': 'user@example.com',
        'amount': 100.0,
    }

    with pytest.raises(HttpNotFoundError):
        controller.operate(request_data, 'user@example.com')
