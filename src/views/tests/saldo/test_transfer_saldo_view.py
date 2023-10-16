import pytest
from unittest.mock import MagicMock, patch
from src.views.saldo.transfer_saldo_view import TransferView
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
def transfer_saldo_view():
    controller = MagicMock()
    view = TransferView(controller)
    return view


def test_handle_success(transfer_saldo_view):
    valid_email = 'user@example.com'
    valid_token = token_creator.create(valid_email)

    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': valid_email,
    }

    http_request = HttpRequest(body={"source_email": valid_email, "target_email": "target@example.com", "amount": 100}, header=headers)

    with patch.object(transfer_saldo_view._TransferView__controller, 'operate') as mock_operate:
        mock_operate.return_value = "Transferência de 100 realizada com sucesso da conta de user@example.com para target@example.com"
        email_and_amount_validator.return_value = None

        response = transfer_saldo_view.handle(http_request)

    mock_operate.assert_called_once_with(
        {
            "source_email": valid_email,
            "target_email": "target@example.com",
            "amount": 100
        },
        valid_email
    )
    assert response.status_code == 200
    assert response.body == {"response": "Transferência de 100 realizada com sucesso da conta de user@example.com para target@example.com"}


def test_handle_exception(transfer_saldo_view):
    valid_email = 'user@example.com'
    valid_token = token_creator.create(valid_email)

    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': valid_email,
    }

    http_request = HttpRequest(body={"source_email": valid_email, "target_email": "target@example.com", "amount": 100}, header=headers)

    with patch.object(transfer_saldo_view._TransferView__controller, 'operate') as mock_operate:
        mock_operate.side_effect = Exception("Test exception")
        email_and_amount_validator.return_value = None

        response = transfer_saldo_view.handle(http_request)

    mock_operate.assert_called_once_with(
        {
            "source_email": valid_email,
            "target_email": "target@example.com",
            "amount": 100
        },
        valid_email
    )
    assert response.status_code == 500
    assert response.body == {"errors": [{"title": "Server Error", "detail": "Test exception"}]}


def test_handle_validation_error(transfer_saldo_view):
    http_request = HttpRequest(body={})
    email_and_amount_validator.side_effect = ValueError("Validation error")

    response = transfer_saldo_view.handle(http_request)

    transfer_saldo_view._TransferView__controller.operate.assert_not_called()
    assert response.status_code == 422


def test_handle_unauthorized_error(transfer_saldo_view):
    valid_email = 'different@example.com'
    valid_token = token_creator.create(valid_email)

    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': 'different@example.com',
    }

    http_request = HttpRequest(body={"source_email": valid_email, "target_email": "target@example.com", "amount": 100},
                               header=headers)

    with patch.object(transfer_saldo_view._TransferView__controller, 'operate') as mock_operate:
        mock_operate.side_effect = HttpUnauthorizedError("Unauthorized")
        response = transfer_saldo_view.handle(http_request)

    mock_operate.assert_called_once_with(
        {
            "source_email": valid_email,
            "target_email": "target@example.com",
            "amount": 100
        },
        valid_email
    )
    assert response.status_code == 401


def test_handle_exception_error(transfer_saldo_view):
    valid_email = 'user@example.com'
    valid_token = token_creator.create(valid_email)

    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': valid_email,
    }

    http_request = HttpRequest(body={"source_email": valid_email, "target_email": "target@example.com", "amount": 100}, header=headers)

    with patch.object(transfer_saldo_view._TransferView__controller, 'operate') as mock_operate:
        mock_operate.side_effect = Exception("Test exception")
        response = transfer_saldo_view.handle(http_request)

    mock_operate.assert_called_once_with(
        {
            "source_email": valid_email,
            "target_email": "target@example.com",
            "amount": 100
        },
        valid_email
    )
    assert response.status_code == 500
    assert response.body == {
        "errors": [{"title": "Server Error", "detail": "Test exception"}]
    }
