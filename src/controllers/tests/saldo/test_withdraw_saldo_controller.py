import pytest
from unittest.mock import MagicMock
from src.controllers.saldo.withdraw_saldo_controller import WithdrawSaldoController
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_insufficient_balance_error import HttpInsufficientBalanceError


@pytest.fixture
def withdraw_saldo_controller():
    account_model = MagicMock()
    saldo_model = MagicMock()
    return WithdrawSaldoController(account_model, saldo_model)


def test_operate_success(withdraw_saldo_controller):
    email = "test@example.com"
    amount = 50

    withdraw_saldo_controller._WithdrawSaldoController__account_model.check_account_exists.return_value = True
    withdraw_saldo_controller._WithdrawSaldoController__saldo_model.check_saldo.return_value = 100

    response = withdraw_saldo_controller.operate({"email": email, "amount": amount}, email)

    withdraw_saldo_controller._WithdrawSaldoController__saldo_model.add_saldo.assert_called_once_with(email, -amount)
    assert response == f"Saque de {amount} realizado com sucesso na conta de {email}"


def test_operate_account_not_found(withdraw_saldo_controller):
    email = "test@example.com"
    amount = 50

    withdraw_saldo_controller._WithdrawSaldoController__account_model.check_account_exists.return_value = False

    with pytest.raises(HttpNotFoundError):
        withdraw_saldo_controller.operate({"email": email, "amount": amount}, email)


def test_operate_insufficient_balance(withdraw_saldo_controller):
    email = "test@example.com"
    amount = 150

    withdraw_saldo_controller._WithdrawSaldoController__account_model.check_account_exists.return_value = True
    withdraw_saldo_controller._WithdrawSaldoController__saldo_model.check_saldo.return_value = 100

    with pytest.raises(HttpInsufficientBalanceError):
        withdraw_saldo_controller.operate({"email": email, "amount": amount}, email)
