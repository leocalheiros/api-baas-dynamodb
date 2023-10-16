from unittest.mock import MagicMock
import pytest
from src.controllers.account.get_account_by_email_controller import GetAccountByEmailController
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_unauthorized import HttpUnauthorizedError


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

    response = get_account_by_email_controller.operate({"email": email}, email)

    get_account_by_email_controller._GetAccountByEmailController__model.get_account_by_email.assert_called_once_with(
        email
    )

    assert 'Conta encontrada' in response


def test_get_account_by_email_nonexistent_email(get_account_by_email_controller):
    email = "nonexistent@example.com"

    get_account_by_email_controller._GetAccountByEmailController__model.check_account_exists.return_value = False

    with pytest.raises(HttpNotFoundError) as exc_info:
        get_account_by_email_controller.operate({"email": email}, email)

    assert str(exc_info.value) == "Conta não existente no banco de dados"


def test_get_account_by_email_unauthorized(get_account_by_email_controller):
    email = "test@example.com"

    with pytest.raises(HttpUnauthorizedError) as exc_info:
        get_account_by_email_controller.operate({"email": "unauthorized@example.com"}, email)

    assert str(exc_info.value) == "Email na solicitação não corresponde ao email nos cabeçalhos!"
