from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse
from src.views.interface.views_interface import ViewInterface
from src.controllers.interface.controller_interface import ControllerInterface
from src.errors.error_handler import handle_errors
from src.validators.create_account_validator import all_fields_validator


class CreateAccountView(ViewInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            account_data = http_request.body
            all_fields_validator(account_data)
            response = self.__controller.operate(account_data)
            return HttpResponse(status_code=200, body={"response": response})
        except Exception as exception:
            return handle_errors(exception)
