from unittest.mock import MagicMock, patch
import pytest
from src.views.pix.pix_view import PixView
from src.views.http_types.http_request import HttpRequest
from src.errors.types.http_bad_request import HttpBadRequest
from src.controllers.interface.pix_controller_interface import PixControllerInterface


class FakePixController(PixControllerInterface):
    def generate_payload(self, chavepix, valor, nome, cidade, txtId):
        return "Generated Payload"

@pytest.fixture
def pix_view():
    controller = FakePixController()
    view = PixView(controller)
    return view


def test_handle_success(pix_view):
    request_data = {
        "chavepix": "+5544997472529",
        "valor": "100.0",
        "nome": "João Silva",
        "cidade": "Cidade",
        "txtId": "txtId"
    }

    http_request = HttpRequest(body=request_data)

    response = pix_view.handle(http_request)

    assert response.status_code == 200
    assert response.body == {"response": "Generated Payload"}


def test_handle_exception(pix_view):
    request_data = {
        "chavepix": "chavepix",
        "valor": "100.0",
        "nome": "Nome do beneficiário",
        "cidade": "Cidade do beneficiário",
        "txtId": "txtId"
    }

    http_request = HttpRequest(body=request_data)

    exception = HttpBadRequest("Bad Request")

    # Usando patch para configurar side_effect corretamente
    with patch.object(pix_view._PixView__controller, 'generate_payload') as mock_generate_payload:
        mock_generate_payload.side_effect = exception
        response = pix_view.handle(http_request)

    assert response.status_code == 400
    assert response.body == {
        "errors": [
            {
                "title": exception.name,
                "detail": exception.message
            }
        ]
    }
