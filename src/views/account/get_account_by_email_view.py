from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse
from src.views.interface.views_interface import ViewInterface
from src.controllers.interface.controller_interface import ControllerInterface
from src.errors.error_handler import handle_errors
from src.validators.email_account_validator import email_field_validator


class GetAccountByEmailView(ViewInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            request_data = http_request.body
            email_field_validator(request_data)
            email = request_data.get("email")
            response = self.__controller.operate(email)
            return HttpResponse(status_code=200, body={"response": response})
        except Exception as exception:
            return handle_errors(exception)
