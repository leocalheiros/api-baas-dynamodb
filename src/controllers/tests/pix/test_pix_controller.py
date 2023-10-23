from unittest.mock import MagicMock
import pytest
from src.controllers.pix.pix_controller import PixController
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError


@pytest.fixture
def pix_controller():
    return PixController()


def test_generate_payload_success(pix_controller):
    chavepix = "chavepix"
    valor = 100.00
    nome = "Nome Teste"
    cidade = "Cidade"
    txtId = "txtId"

    payload = pix_controller.generate_payload(chavepix, valor, nome, cidade, txtId)

    assert payload


def test_generate_payload_invalid_valor(pix_controller):
    chavepix = "chavepix"
    valor = -10.0  # Valor inválido
    nome = "Nome Teste"
    cidade = "Cidade"
    txtId = "txtId"

    with pytest.raises(HttpUnprocessableEntityError):
        pix_controller.generate_payload(chavepix, valor, nome, cidade, txtId)
