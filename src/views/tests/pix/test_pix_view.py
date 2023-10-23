from unittest.mock import MagicMock
import pytest
from src.views.pix.pix_view import PixView
from src.views.http_types.http_request import HttpRequest
from src.errors.types.http_bad_request import HttpBadRequest
from src.views.http_types.http_response import HttpResponse


@pytest.fixture
def pix_view():
    controller = MagicMock()
    return PixView(controller)


def test_handle_success(pix_view):
    request_data = {
        "chavepix": "chavepix",
        "valor": 100.0,
        "nome": "Nome do beneficiário",
        "cidade": "Cidade do beneficiário",
        "txtId": "txtId"
    }

    http_request = HttpRequest(body=request_data)

    pix_view._PixView__controller.generate_payload.return_value = "Generated Payload"

    response = pix_view.handle(http_request)

    pix_view._PixView__controller.generate_payload.assert_called_once()

    assert response.status_code == 200
    assert response.body == {"response": "Generated Payload"}


def test_handle_exception(pix_view):
    request_data = {
        "chavepix": "chavepix",
        "valor": 100.0,
        "nome": "Nome do beneficiário",
        "cidade": "Cidade do beneficiário",
        "txtId": "txtId"
    }

    http_request = HttpRequest(body=request_data)

    exception = HttpBadRequest("Bad Request")

    pix_view._PixView__controller.generate_payload.side_effect = exception

    response = pix_view.handle(http_request)

    pix_view._PixView__controller.generate_payload.assert_called_once()

    assert response.status_code == 400
    assert response.body == {
        "errors": [
            {
                "title": exception.name,
                "detail": exception.message
            }
        ]
    }


def test_handle_validator_error(pix_view):
    request_data = {
        "chavepix": "",  # Chave vazia para disparar uma exceção de validação
        "valor": 100.0,
        "nome": "Nome do beneficiário",
        "cidade": "Cidade do beneficiário",
        "txtId": "txtId"
    }

    http_request = HttpRequest(body=request_data)

    pix_view._PixView__controller.generate_payload.return_value = "Generated Payload"

    response = pix_view.handle(http_request)

    pix_view._PixView__controller.generate_payload.assert_not_called()

    assert response.status_code == 422
