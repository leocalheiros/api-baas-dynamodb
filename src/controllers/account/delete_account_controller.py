from src.models.interface.account_interface import AccountRepositoryInterface
from src.controllers.interface.account_controller_interface import ControllerInterface
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_unauthorized import HttpUnauthorizedError


class DeleteAccountController(ControllerInterface):
    def __init__(self, model: AccountRepositoryInterface):
        self.__model = model

    def operate(self, account: dict, request_email: str) -> dict:
        email = account.get("email")
        self.__validate(email, request_email)
        self.__model.delete_account(email)
        return self.__format_response(email)

    def __validate(self, email: str, request_email: str) -> None:
        if email != request_email:
            raise HttpUnauthorizedError("Email na solicitação não corresponde ao email nos cabeçalhos!")
        if not self.__model.check_account_exists(email):
            raise HttpNotFoundError("Email não existente no banco de dados!")

    def __format_response(self, email) -> dict:
        return {
            "data": {
                "status": "success",
                "email": email
            }
        }
