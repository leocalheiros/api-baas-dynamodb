import pytest
from unittest.mock import MagicMock
from src.views.saldo.deposit_saldo_view import DepositView
from src.views.http_types.http_request import HttpRequest
from src.validators.saldo.email_and_amount_validator import email_and_amount_validator


@pytest.fixture
def deposit_saldo_view():
    controller = MagicMock()
    return DepositView(controller)


def test_handle_success(deposit_saldo_view):
    http_request = HttpRequest(body={"email": "test@example.com", "amount": 100})
    deposit_saldo_view._DepositView__controller.operate.return_value = "Depósito de 100 realizado com sucesso na conta de test@example.com"
    email_and_amount_validator.return_value = None

    response = deposit_saldo_view.handle(http_request)

    deposit_saldo_view._DepositView__controller.operate.assert_called_once_with(http_request.body.get("email"), http_request.body.get("amount"))
    assert response.status_code == 200
    assert response.body == {"response": "Depósito de 100 realizado com sucesso na conta de test@example.com"}


def test_handle_exception(deposit_saldo_view):
    http_request = HttpRequest(body={"email": "test@example.com", "amount": 100})
    deposit_saldo_view._DepositView__controller.operate.side_effect = Exception("Test exception")
    email_and_amount_validator.return_value = None

    response = deposit_saldo_view.handle(http_request)

    deposit_saldo_view._DepositView__controller.operate.assert_called_once_with(http_request.body.get("email"), http_request.body.get("amount"))
    assert response.status_code == 500
    assert response.body == {"errors": [{"title": "Server Error", "detail": "Test exception"}]}


def test_handle_validation_error(deposit_saldo_view):
    http_request = HttpRequest(body={})
    email_and_amount_validator.side_effect = ValueError("Validation error")

    response = deposit_saldo_view.handle(http_request)

    deposit_saldo_view._DepositView__controller.operate.assert_not_called()
    assert response.status_code == 422
