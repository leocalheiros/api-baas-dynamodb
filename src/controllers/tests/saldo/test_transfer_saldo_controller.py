import pytest
from unittest.mock import MagicMock
from src.controllers.saldo.transfer_saldo_controller import TransferSaldoController
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_insufficient_balance_error import HttpInsufficientBalanceError
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError


@pytest.fixture
def transfer_saldo_controller():
    account_model = MagicMock()
    saldo_model = MagicMock()
    return TransferSaldoController(account_model, saldo_model)


def test_operate_success(transfer_saldo_controller):
    source_email = "source@example.com"
    target_email = "target@example.com"
    amount = 100

    transfer_saldo_controller._TransferSaldoController__account_model.check_account_exists.side_effect = [True, True]
    transfer_saldo_controller._TransferSaldoController__saldo_model.check_saldo.return_value = 150

    response = transfer_saldo_controller.operate({"source_email": source_email, "target_email": target_email, "amount": amount}, source_email)

    transfer_saldo_controller._TransferSaldoController__saldo_model.add_saldo.assert_any_call(target_email, amount)
    transfer_saldo_controller._TransferSaldoController__saldo_model.add_saldo.assert_any_call(source_email, -amount)

    expected_response = {
            "data": {
                "status": "success",
                "source_email": source_email,
                "target_email": target_email,
                "amount": amount
            }
        }

    assert response == expected_response


def test_operate_source_account_not_found(transfer_saldo_controller):
    source_email = "source@example.com"
    target_email = "target@example.com"
    amount = 100

    transfer_saldo_controller._TransferSaldoController__account_model.check_account_exists.return_value = False

    with pytest.raises(HttpNotFoundError):
        transfer_saldo_controller.operate({"source_email": source_email, "target_email": target_email, "amount": amount}, source_email)


def test_operate_target_account_not_found(transfer_saldo_controller):
    source_email = "source@example.com"
    target_email = "target@example.com"
    amount = 100

    transfer_saldo_controller._TransferSaldoController__account_model.check_account_exists.side_effect = [True, False]

    with pytest.raises(HttpNotFoundError):
        transfer_saldo_controller.operate({"source_email": source_email, "target_email": target_email, "amount": amount}, source_email)


def test_operate_insufficient_balance(transfer_saldo_controller):
    source_email = "source@example.com"
    target_email = "target@example.com"
    amount = 100

    transfer_saldo_controller._TransferSaldoController__account_model.check_account_exists.side_effect = [True, True]
    transfer_saldo_controller._TransferSaldoController__saldo_model.check_saldo.return_value = 50

    with pytest.raises(HttpInsufficientBalanceError):
        transfer_saldo_controller.operate({"source_email": source_email, "target_email": target_email, "amount": amount}, source_email)
