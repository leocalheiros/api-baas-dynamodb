import pytest
from unittest.mock import Mock, patch
from src.views.payments.create_credit_card_payment_view import CreateCreditCardPaymentView
from src.controllers.payments.create_credit_card_payment_controller import TransactionController
from src.models.interface.account_interface import AccountRepositoryInterface
from src.models.interface.credit_card_interface import CreditCardRepositoryInterface
from src.middlewares.auth_jwt.token_creator import TokenCreator
from src.errors.types.http_bad_request import HttpBadRequest
from src.views.http_types.http_request import HttpRequest

TOKEN_KEY = '1234'
EXP_TIME_MIN = 60
REFRESH_TIME_MIN = 30
token_creator = TokenCreator(TOKEN_KEY, EXP_TIME_MIN, REFRESH_TIME_MIN)


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


@pytest.fixture
def create_credit_card_payment_view():
    account_model_mock = create_account_model_mock(exists=True)
    controller = TransactionController(account_model_mock, create_card_model_mock(has_credit_card=True))
    view = CreateCreditCardPaymentView(controller)
    return view


def test_create_credit_card_payment_view_success(create_credit_card_payment_view):
    valid_email = 'user@example.com'
    valid_token = token_creator.create(valid_email)

    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': valid_email,
    }

    request_data = {
        'email': valid_email,
        'amount': 100,
    }

    http_request = HttpRequest(body=request_data, header=headers)

    with patch.object(create_credit_card_payment_view._CreateCreditCardPaymentView__controller, 'operate') as mock_operate:
        mock_operate.return_value = {
            "status": "success",
            "email": valid_email,
            "amount": 100,
            "card_number": "4134185779995000"
        }

        response = create_credit_card_payment_view.handle(http_request)
        assert response.status_code == 200
        assert response.body == {
            "response": {
                "status": "success",
                "email": valid_email,
                "amount": 100,
                "card_number": "4134185779995000"
            }
        }


def test_create_credit_card_payment_view_exception(create_credit_card_payment_view):
    valid_email = 'user@example.com'
    valid_token = token_creator.create(valid_email)

    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': valid_email,
    }

    request_data = {
        'email': valid_email,
        'amount': 100,
    }

    http_request = HttpRequest(body=request_data, header=headers)

    with patch.object(create_credit_card_payment_view._CreateCreditCardPaymentView__controller, 'operate') as mock_operate:
        exception = HttpBadRequest("Bad Request")
        mock_operate.side_effect = exception

        response = create_credit_card_payment_view.handle(http_request)

    mock_operate.assert_called_once_with(
        {
            "email": valid_email,
            "amount": 100,
        },
        valid_email
    )
    assert response.status_code == 400
    assert response.body == {
        "errors": [{"title": exception.name, "detail": exception.message}]
    }
