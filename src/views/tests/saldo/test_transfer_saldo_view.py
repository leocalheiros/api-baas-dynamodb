import pytest
from unittest.mock import MagicMock
from src.views.saldo.transfer_saldo_view import TransferView
from src.views.http_types.http_request import HttpRequest
from src.validators.saldo.all_fields_validator import all_fields_validator


@pytest.fixture
def transfer_saldo_view():
    controller = MagicMock()
    return TransferView(controller)


def test_handle_success(transfer_saldo_view):
    http_request = HttpRequest(body={"source_email": "source@example.com", "target_email": "target@example.com", "amount": 100})
    transfer_saldo_view._TransferView__controller.operate.return_value = "Transferência de 100 realizada com sucesso da conta de source@example.com para target@example.com"
    all_fields_validator.return_value = None

    response = transfer_saldo_view.handle(http_request)

    transfer_saldo_view._TransferView__controller.operate.assert_called_once_with(http_request.body.get("source_email"), http_request.body.get("target_email"), http_request.body.get("amount"))
    assert response.status_code == 200
    assert response.body == {"response": "Transferência de 100 realizada com sucesso da conta de source@example.com para target@example.com"}


def test_handle_exception(transfer_saldo_view):
    http_request = HttpRequest(body={"source_email": "source@example.com", "target_email": "target@example.com", "amount": 100})
    transfer_saldo_view._TransferView__controller.operate.side_effect = Exception("Test exception")
    all_fields_validator.return_value = None

    response = transfer_saldo_view.handle(http_request)

    transfer_saldo_view._TransferView__controller.operate.assert_called_once_with(http_request.body.get("source_email"), http_request.body.get("target_email"), http_request.body.get("amount"))
    assert response.status_code == 500
    assert response.body == {"errors": [{"title": "Server Error", "detail": "Test exception"}]}


def test_handle_validation_error(transfer_saldo_view):
    http_request = HttpRequest(body={})
    all_fields_validator.side_effect = ValueError("Validation error")

    response = transfer_saldo_view.handle(http_request)

    transfer_saldo_view._TransferView__controller.operate.assert_not_called()
    assert response.status_code == 422
