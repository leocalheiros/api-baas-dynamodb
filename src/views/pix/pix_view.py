from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse
from src.views.interface.views_interface import ViewInterface
from src.controllers.interface.pix_controller_interface import PixControllerInterface
from src.errors.error_handler import handle_errors


class PixView(ViewInterface):
    def __init__(self, controller: PixControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            request_data = http_request.body
            chavepix = request_data.get("chavepix")
            valor = float(request_data.get("valor"))
            nome = request_data.get("nome")
            cidade = request_data.get("cidade")
            txtId = request_data.get("txtId")
            response = self.__controller.generate_payload(chavepix, valor, nome, cidade, txtId)
            return HttpResponse(status_code=200, body={"response": response})
        except Exception as exception:
            return handle_errors(exception)
