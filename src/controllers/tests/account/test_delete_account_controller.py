from unittest.mock import MagicMock
import pytest
from src.controllers.account.delete_account_controller import DeleteAccountController
from src.errors.types.http_not_found import HttpNotFoundError


@pytest.fixture
def delete_account_controller():
    model = MagicMock()
    model.check_account_exists.return_value = True
    return DeleteAccountController(model)


def test_delete_account_success(delete_account_controller):
    account_data = {
        "email": "test@example.com"
    }

    response = delete_account_controller.operate(account_data)

    delete_account_controller._DeleteAccountController__model.delete_account.assert_called_once_with(
        "test@example.com"
    )

    assert response == "Conta deletada com sucesso!"


def test_delete_account_nonexistent_email(delete_account_controller):
    account_data = {
        "email": "nonexistent@example.com"
    }

    delete_account_controller._DeleteAccountController__model.check_account_exists.return_value = False

    with pytest.raises(HttpNotFoundError) as exc_info:
        delete_account_controller.operate(account_data)

    assert str(exc_info.value) == "Email não existente no banco de dados!"