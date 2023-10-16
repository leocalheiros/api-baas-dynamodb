import pytest
from unittest.mock import MagicMock, patch
from src.views.account.delete_account_view import DeleteAccountView
from src.views.http_types.http_request import HttpRequest
from src.validators.account.email_account_validator import email_field_validator
from src.middlewares.auth_jwt.token_creator import TokenCreator

# Configurar o TokenCreator para os testes
TOKEN_KEY = '1234'
EXP_TIME_MIN = 60
REFRESH_TIME_MIN = 30
token_creator = TokenCreator(TOKEN_KEY, EXP_TIME_MIN, REFRESH_TIME_MIN)


@pytest.fixture
def delete_account_view():
    controller = MagicMock()
    view = DeleteAccountView(controller)
    return view


def test_handle_success(delete_account_view):
    # Crie um token JWT válido com o email associado
    valid_email = 'user@example.com'
    valid_token = token_creator.create(valid_email)

    # Configure o cabeçalho da solicitação com o token JWT e o email
    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': valid_email,
    }

    # Crie uma instância HttpRequest simulando a solicitação com o cabeçalho correto
    http_request = HttpRequest(body={"email": valid_email}, header=headers)

    # Patchear o método operate do controller para verificar se ele foi chamado
    with patch.object(delete_account_view._DeleteAccountView__controller, 'operate') as mock_operate:
        mock_operate.return_value = "Conta deletada com sucesso!"
        response = delete_account_view.handle(http_request)

    # Verifique se o método operate foi chamado no objeto de controle
    mock_operate.assert_called_once_with(http_request.body, valid_email)


def test_handle_exception(delete_account_view):
    # Crie um token JWT válido com o email associado
    valid_email = 'user@example.com'
    valid_token = token_creator.create(valid_email)

    # Configure o cabeçalho da solicitação com o token JWT e o email
    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': valid_email,
    }

    # Crie uma instância HttpRequest simulando a solicitação com o cabeçalho correto
    http_request = HttpRequest(body={"email": valid_email}, header=headers)

    # Patchear o método operate do controller para lançar uma exceção
    with patch.object(delete_account_view._DeleteAccountView__controller, 'operate') as mock_operate:
        mock_operate.side_effect = Exception("Test exception")
        response = delete_account_view.handle(http_request)

    # Verifique se o método operate foi chamado no objeto de controle
    mock_operate.assert_called_once_with(http_request.body, valid_email)
    assert response.status_code == 500
    assert response.body == {
        "errors": [{"title": "Server Error", "detail": "Test exception"}]
    }
