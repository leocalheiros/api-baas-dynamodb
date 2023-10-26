from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse
from src.views.interface.views_interface import ViewInterface
from src.controllers.interface.account_controller_interface import ControllerInterface
from src.errors.error_handler import handle_errors
from src.validators.payments.delete_credit_card_validator import delete_credit_card_fields


class DeleteCreditCardView(ViewInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            request_data = http_request.body
            delete_credit_card_fields(request_data)
            request_email = http_request.header.get("email")
            response = self.__controller.operate(request_data, request_email)
            return HttpResponse(status_code=200, body={"response": response})
        except Exception as exception:
            return handle_errors(exception)
