import pytest
from unittest.mock import MagicMock
from src.views.account.delete_account_view import DeleteAccountView
from src.views.http_types.http_request import HttpRequest
from src.validators.email_account_validator import email_field_validator


@pytest.fixture
def delete_account_view():
    controller = MagicMock()
    return DeleteAccountView(controller)


def test_handle_success(delete_account_view):
    http_request = HttpRequest(body={"email": "test@example.com"})
    delete_account_view._DeleteAccountView__controller.operate.return_value = "Conta deletada com sucesso!"
    email_field_validator.return_value = None

    response = delete_account_view.handle(http_request)

    delete_account_view._DeleteAccountView__controller.operate.assert_called_once_with(http_request.body)
    assert response.status_code == 200
    assert response.body == {"response": "Conta deletada com sucesso!"}


def test_handle_exception(delete_account_view):
    http_request = HttpRequest(body={"email": "test@example.com"})
    delete_account_view._DeleteAccountView__controller.operate.side_effect = Exception("Test exception")
    email_field_validator.return_value = None

    response = delete_account_view.handle(http_request)

    delete_account_view._DeleteAccountView__controller.operate.assert_called_once_with(http_request.body)
    assert response.status_code == 500
    assert response.body == {"errors": [{"title": "Server Error", "detail": "Test exception"}]}


def test_handle_validation_error(delete_account_view):
    http_request = HttpRequest(body={})
    email_field_validator.side_effect = ValueError("Validation error")

    response = delete_account_view.handle(http_request)

    delete_account_view._DeleteAccountView__controller.operate.assert_not_called()
    assert response.status_code == 422
