import pytest
from unittest.mock import MagicMock, patch
from src.views.saldo.withdraw_saldo_view import WithdrawView
from src.views.http_types.http_request import HttpRequest
from src.validators.saldo.email_and_amount_validator import email_and_amount_validator
from src.errors.types.http_unauthorized import HttpUnauthorizedError
from src.middlewares.auth_jwt.token_creator import TokenCreator

# Configurar o TokenCreator para os testes
TOKEN_KEY = '1234'
EXP_TIME_MIN = 60
REFRESH_TIME_MIN = 30
token_creator = TokenCreator(TOKEN_KEY, EXP_TIME_MIN, REFRESH_TIME_MIN)


@pytest.fixture
def withdraw_saldo_view():
    controller = MagicMock()
    view = WithdrawView(controller)
    return view


def test_handle_success(withdraw_saldo_view):
    valid_email = 'user@example.com'
    valid_token = token_creator.create(valid_email)

    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': valid_email,
    }

    http_request = HttpRequest(body={"email": valid_email, "amount": 100}, header=headers)

    with patch.object(withdraw_saldo_view._WithdrawView__controller, 'operate') as mock_operate:
        mock_operate.return_value = "Saque de 100 realizado com sucesso na conta de user@example.com"
        email_and_amount_validator.return_value = None

        response = withdraw_saldo_view.handle(http_request)

    mock_operate.assert_called_once_with(
        {
            "email": valid_email,
            "amount": 100
        },
        valid_email
    )
    assert response.status_code == 200
    assert response.body == {"response": "Saque de 100 realizado com sucesso na conta de user@example.com"}


def test_handle_exception(withdraw_saldo_view):
    valid_email = 'user@example.com'
    valid_token = token_creator.create(valid_email)

    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': valid_email,
    }

    http_request = HttpRequest(body={"email": valid_email, "amount": 100}, header=headers)

    with patch.object(withdraw_saldo_view._WithdrawView__controller, 'operate') as mock_operate:
        mock_operate.side_effect = Exception("Test exception")
        email_and_amount_validator.return_value = None

        response = withdraw_saldo_view.handle(http_request)

    mock_operate.assert_called_once_with(
        {
            "email": valid_email,
            "amount": 100
        },
        valid_email
    )
    assert response.status_code == 500
    assert response.body == {"errors": [{"title": "Server Error", "detail": "Test exception"}]}

def test_handle_validation_error(withdraw_saldo_view):
    http_request = HttpRequest(body={})
    email_and_amount_validator.side_effect = ValueError("Validation error")

    response = withdraw_saldo_view.handle(http_request)

    withdraw_saldo_view._WithdrawView__controller.operate.assert_not_called()
    assert response.status_code == 422


def test_handle_unauthorized_error(withdraw_saldo_view):
    valid_email = 'different@example.com'
    valid_token = token_creator.create(valid_email)

    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': 'different@example.com',
    }

    http_request = HttpRequest(body={"email": valid_email, "amount": 100}, header=headers)

    with patch.object(withdraw_saldo_view._WithdrawView__controller, 'operate') as mock_operate:
        mock_operate.side_effect = HttpUnauthorizedError("Unauthorized")
        response = withdraw_saldo_view.handle(http_request)

    mock_operate.assert_called_once_with(
        {
            "email": valid_email,
            "amount": 100
        },
        valid_email
    )
    assert response.status_code == 401


def test_handle_exception_error(withdraw_saldo_view):
    valid_email = 'user@example.com'
    valid_token = token_creator.create(valid_email)

    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': valid_email,
    }

    http_request = HttpRequest(body={"email": valid_email, "amount": 100}, header=headers)

    with patch.object(withdraw_saldo_view._WithdrawView__controller, 'operate') as mock_operate:
        mock_operate.side_effect = Exception("Test exception")
        response = withdraw_saldo_view.handle(http_request)

    mock_operate.assert_called_once_with(
        {
            "email": valid_email,
            "amount": 100
        },
        valid_email
    )
    assert response.status_code == 500
    assert response.body == {
        "errors": [{"title": "Server Error", "detail": "Test exception"}]
    }
