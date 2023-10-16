import pytest
from unittest.mock import MagicMock, patch
from src.views.account.get_account_by_email_view import GetAccountByEmailView
from src.views.http_types.http_request import HttpRequest
from src.middlewares.auth_jwt.token_creator import TokenCreator

# Configurar o TokenCreator para os testes
TOKEN_KEY = '1234'
EXP_TIME_MIN = 60
REFRESH_TIME_MIN = 30
token_creator = TokenCreator(TOKEN_KEY, EXP_TIME_MIN, REFRESH_TIME_MIN)


@pytest.fixture
def get_account_by_email_view():
    controller = MagicMock()
    view = GetAccountByEmailView(controller)
    return view


def test_handle_success(get_account_by_email_view):
    valid_email = 'user@example.com'
    valid_token = token_creator.create(valid_email)

    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': valid_email,
    }

    http_request = HttpRequest(body={"email": valid_email}, header=headers)

    with patch.object(get_account_by_email_view._GetAccountByEmailView__controller, 'operate') as mock_operate:
        mock_operate.return_value = "Conta encontrada: user@example.com"
        response = get_account_by_email_view.handle(http_request)

    mock_operate.assert_called_once_with({'email': 'user@example.com'}, 'user@example.com')


def test_handle_exception(get_account_by_email_view):
    valid_email = 'user@example.com'
    valid_token = token_creator.create(valid_email)

    headers = {
        'Authorization': f'Bearer {valid_token}',
        'email': valid_email,
    }

    http_request = HttpRequest(body={"email": valid_email}, header=headers)

    with patch.object(get_account_by_email_view._GetAccountByEmailView__controller, 'operate') as mock_operate:
        mock_operate.side_effect = Exception("Test exception")
        response = get_account_by_email_view.handle(http_request)

    mock_operate.assert_called_once_with({'email': 'user@example.com'}, 'user@example.com')
    assert response.status_code == 500
    assert response.body == {"errors": [{"title": "Server Error", "detail": "Test exception"}]}
