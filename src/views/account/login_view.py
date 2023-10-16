from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse
from src.views.interface.views_interface import ViewInterface
from src.controllers.interface.account_controller_interface import ControllerInterface
from src.errors.error_handler import handle_errors
from src.validators.account.email_and_senha_validator import email_and_senha_validator


class LoginAccountView(ViewInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            request_data = http_request.body
            email_and_senha_validator(request_data)
            email = request_data.get("email")
            senha = request_data.get("senha")
            response = self.__controller.operate(email, senha)
            return HttpResponse(status_code=200, body={"response": response})
        except Exception as exception:
            return handle_errors(exception)
