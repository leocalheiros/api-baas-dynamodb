from unittest.mock import MagicMock
import pytest
from src.controllers.saldo.deposit_saldo_controller import DepositSaldoController
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError


@pytest.fixture
def deposit_saldo_controller():
    account_model = MagicMock()
    saldo_model = MagicMock()
    return DepositSaldoController(account_model, saldo_model)


def test_operate_success(deposit_saldo_controller):
    email = "test@example.com"
    amount = 100

    deposit_saldo_controller._DepositSaldoController__account_model.check_account_exists.return_value = True

    response = deposit_saldo_controller.operate({"email": email, "amount": amount}, email)

    deposit_saldo_controller._DepositSaldoController__saldo_model.add_saldo.assert_called_once_with(email, amount)

    expected_response = {
        "data": {
            "status": "success",
            "amount": amount,
            "email": email
        }
    }

    assert response == expected_response


def test_operate_account_not_found(deposit_saldo_controller):
    email = "test@example.com"
    amount = 100

    deposit_saldo_controller._DepositSaldoController__account_model.check_account_exists.return_value = False

    with pytest.raises(HttpNotFoundError):
        deposit_saldo_controller.operate({"email": email, "amount": amount}, email)

