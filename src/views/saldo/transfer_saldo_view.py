from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse
from src.views.interface.views_interface import ViewInterface
from src.controllers.interface.saldo_controller_interface import SaldoControllerInterface
from src.errors.error_handler import handle_errors
from src.validators.saldo.all_fields_validator import all_fields_validator


class TransferView(ViewInterface):
    def __init__(self, controller: SaldoControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            request_data = http_request.body
            all_fields_validator(request_data)
            source_email = request_data.get("source_email")
            target_email = request_data.get("target_email")
            amount = request_data.get("amount")
            response = self.__controller.operate(source_email, target_email, amount)
            return HttpResponse(status_code=200, body={"response": response})
        except Exception as exception:
            return handle_errors(exception)
