from unittest.mock import MagicMock
import pytest
from src.controllers.account.get_account_by_email_controller import GetAccountByEmailController
from src.errors.types.http_not_found import HttpNotFoundError


@pytest.fixture
def get_account_by_email_controller():
    model = MagicMock()
    model.check_account_exists.return_value = True
    model.get_account_by_email.return_value = {
        "email": "test@example.com",
        "saldo": 100
    }
    return GetAccountByEmailController(model)


def test_get_account_by_email_success(get_account_by_email_controller):
    email = "test@example.com"

    response = get_account_by_email_controller.operate(email)

    get_account_by_email_controller._GetAccountByEmailController__model.get_account_by_email.assert_called_once_with(
        email
    )

    assert response in ['Conta encontrada: {"email": "test@example.com", "saldo": 100}',
                        'Conta encontrada: {\'email\': \'test@example.com\', \'saldo\': 100}']


def test_get_account_by_email_nonexistent_email(get_account_by_email_controller):
    email = "nonexistent@example.com"

    get_account_by_email_controller._GetAccountByEmailController__model.check_account_exists.return_value = False

    with pytest.raises(HttpNotFoundError) as exc_info:
        get_account_by_email_controller.operate(email)

    assert str(exc_info.value) == "Conta não existente no banco de dados"
