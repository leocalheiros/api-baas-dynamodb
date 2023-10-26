import pytest
from unittest.mock import Mock, patch
from src.views.payments.register_credit_card_view import RegisterCardView
from src.models.interface.account_interface import AccountRepositoryInterface
from src.models.interface.credit_card_interface import CreditCardRepositoryInterface
from src.middlewares.auth_jwt.token_creator import TokenCreator
from src.controllers.payments.register_credit_card_controller import RegisterCardController
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


def create_card_model_mock():
    return Mock(spec=CreditCardRepositoryInterface)


@pytest.fixture
def register_card_view():
    account_model_mock = create_account_model_mock(exists=True)
    controller = RegisterCardController(account_model_mock, create_card_model_mock())
    view = RegisterCardView(controller)
    return view


def test_register_card_view_success(register_card_view):
    valid_email = 'user@example.com'
    valid_token = token_creator.create(valid_email)

    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': valid_email,
    }

    request_data = {
        'email': valid_email,
        'card_number': '4111111111111111',
        'expiration_month': 12,
        'expiration_year': 2025,
        'security_code': '123',
        'holder_name': 'John Doe',
    }

    http_request = HttpRequest(body=request_data, header=headers)

    with patch.object(register_card_view._RegisterCardView__controller, 'operate') as mock_operate:
        mock_operate.return_value = {"status": "success", "email": valid_email}

        response = register_card_view.handle(http_request)

    mock_operate.assert_called_once_with(
        {
            "email": valid_email,
            "card_number": '4111111111111111',
            "expiration_month": 12,
            "expiration_year": 2025,
            "security_code": '123',
            "holder_name": 'John Doe'
        },
        valid_email
    )
    assert response.status_code == 200
    assert response.body == {"response": {"status": "success", "email": valid_email}}


def test_register_card_view_exception(register_card_view):
    valid_email = 'user@example.com'
    valid_token = token_creator.create(valid_email)

    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': valid_email,
    }

    request_data = {
        'email': valid_email,
        'card_number': '4111111111111111',
        'expiration_month': 12,
        'expiration_year': 2025,
        'security_code': '123',
        'holder_name': 'John Doe',
    }

    http_request = HttpRequest(body=request_data, header=headers)

    with patch.object(register_card_view._RegisterCardView__controller, 'operate') as mock_operate:
        exception = HttpBadRequest("Bad Request")
        mock_operate.side_effect = exception

        response = register_card_view.handle(http_request)

    mock_operate.assert_called_once_with(
        {
            "email": valid_email,
            "card_number": '4111111111111111',
            "expiration_month": 12,
            "expiration_year": 2025,
            "security_code": '123',
            "holder_name": 'John Doe'
        },
        valid_email
    )
    assert response.status_code == 400
    assert response.body == {
        "errors": [{"title": exception.name, "detail": exception.message}]
    }
