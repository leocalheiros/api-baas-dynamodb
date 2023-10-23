from pix_utils import Code
from src.controllers.interface.pix_controller_interface import PixControllerInterface
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError


class PixController(PixControllerInterface):
    def generate_payload(self, chavepix, valor, nome, cidade, txtId):
        chavepix = self.format_chave_pix(chavepix)
        valor = self.validate_valor(valor)

        payload = Code(key=chavepix, name=nome, city=cidade, value=valor, identifier=txtId)
        return payload

    def validate_valor(self, valor):
        if valor <= 0:
            raise HttpUnprocessableEntityError("O valor deve ser maior que 0")
        return valor

    def format_chave_pix(self, chavepix):
        chavepix = chavepix.replace(".", "").replace("-", "").replace("/", "").replace("\\", "").replace(" ", "")
        return chavepix
