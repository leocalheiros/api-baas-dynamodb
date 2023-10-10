import pytest
from unittest.mock import MagicMock
from src.views.account.create_account_view import CreateAccountView
from src.views.http_types.http_request import HttpRequest
from src.validators.create_account_validator import all_fields_validator


@pytest.fixture
def create_account_view():
    controller = MagicMock()
    return CreateAccountView(controller)


def test_handle_success(create_account_view):
    http_request = HttpRequest(body={"email": "test@example.com", "senha": "password", "saldo": 100})
    create_account_view._CreateAccountView__controller.operate.return_value = "Usuário criado com sucesso!"
    all_fields_validator.return_value = None

    response = create_account_view.handle(http_request)

    create_account_view._CreateAccountView__controller.operate.assert_called_once_with(http_request.body)
    assert response.status_code == 200
    assert response.body == {"response": "Usuário criado com sucesso!"}


def test_handle_exception(create_account_view):
    http_request = HttpRequest(body={"email": "test@example.com", "senha": "password", "saldo": 100})
    create_account_view._CreateAccountView__controller.operate.side_effect = Exception("Test exception")
    all_fields_validator.return_value = None

    response = create_account_view.handle(http_request)

    create_account_view._CreateAccountView__controller.operate.assert_called_once_with(http_request.body)
    assert response.status_code == 500
    assert response.body == {"errors": [{"title": "Server Error", "detail": "Test exception"}]}


def test_handle_validation_error(create_account_view):
    http_request = HttpRequest(body={})

    response = create_account_view.handle(http_request)

    create_account_view._CreateAccountView__controller.operate.assert_not_called()
    assert response.status_code == 422
