import pytest
from unittest.mock import MagicMock
from src.views.account.get_account_by_email_view import GetAccountByEmailView
from src.views.http_types.http_request import HttpRequest
from src.validators.email_account_validator import email_field_validator


@pytest.fixture
def get_account_by_email_view():
    controller = MagicMock()
    return GetAccountByEmailView(controller)


def test_handle_success(get_account_by_email_view):
    http_request = HttpRequest(body={"email": "test@example.com"})
    get_account_by_email_view._GetAccountByEmailView__controller.operate.return_value = "Conta encontrada: {'email': 'test@example.com', 'saldo': 100}"
    email_field_validator.return_value = None

    response = get_account_by_email_view.handle(http_request)

    get_account_by_email_view._GetAccountByEmailView__controller.operate.assert_called_once_with(http_request.body.get("email"))
    assert response.status_code == 200
    assert response.body == {"response": "Conta encontrada: {'email': 'test@example.com', 'saldo': 100}"}


def test_handle_exception(get_account_by_email_view):
    http_request = HttpRequest(body={"email": "test@example.com"})
    get_account_by_email_view._GetAccountByEmailView__controller.operate.side_effect = Exception("Test exception")
    email_field_validator.return_value = None

    response = get_account_by_email_view.handle(http_request)

    get_account_by_email_view._GetAccountByEmailView__controller.operate.assert_called_once_with(http_request.body.get("email"))
    assert response.status_code == 500
    assert response.body == {"errors": [{"title": "Server Error", "detail": "Test exception"}]}


def test_handle_validation_error(get_account_by_email_view):
    http_request = HttpRequest(body={})
    email_field_validator.side_effect = ValueError("Validation error")

    response = get_account_by_email_view.handle(http_request)

    get_account_by_email_view._GetAccountByEmailView__controller.operate.assert_not_called()
    assert response.status_code == 422
