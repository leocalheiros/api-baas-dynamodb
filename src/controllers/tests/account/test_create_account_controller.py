from unittest.mock import MagicMock
import pytest
from src.controllers.account.create_account_controller import CreateAccountController
from src.errors.types.http_not_found import HttpNotFoundError


@pytest.fixture
def account_controller():
    model = MagicMock()
    model.check_account_exists.return_value = False
    return CreateAccountController(model)


def test_create_account_success(account_controller):
    account_data = {
        "email": "test@example.com",
        "senha": "password",
        "saldo": 100
    }

    response = account_controller.operate(account_data)

    account_controller._CreateAccountController__model.create_account.assert_called_once_with(
        "test@example.com", "password", 100
    )

    expected_response = {
        "status": "success",
        "data": account_data
    }

    assert response == expected_response


def test_create_account_existing_email(account_controller):
    account_data = {
        "email": "existing@example.com",
        "senha": "password",
        "saldo": 50.0
    }

    account_controller._CreateAccountController__model.check_account_exists.return_value = True

    with pytest.raises(HttpNotFoundError) as exc_info:
        account_controller.operate(account_data)

    assert str(exc_info.value) == "Email já existente no banco de dados!"
