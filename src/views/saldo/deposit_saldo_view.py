from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse
from src.views.interface.views_interface import ViewInterface
from src.controllers.interface.saldo_controller_interface import SaldoControllerInterface
from src.errors.error_handler import handle_errors
from src.validators.saldo.email_and_amount_validator import email_and_amount_validator


class DepositView(ViewInterface):
    def __init__(self, controller: SaldoControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            request_data = http_request.body
            email_and_amount_validator(request_data)
            request_email = http_request.header.get("email")
            response = self.__controller.operate(request_data, request_email)
            return HttpResponse(status_code=200, body={"response": response})
        except Exception as exception:
            return handle_errors(exception)
