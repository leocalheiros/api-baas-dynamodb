from src.models.interface.account_interface import AccountRepositoryInterface
from src.controllers.interface.account_controller_interface import ControllerInterface
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_unauthorized import HttpUnauthorizedError


class DeleteAccountController(ControllerInterface):
    def __init__(self, model: AccountRepositoryInterface):
        self.__model = model

    def operate(self, account: dict, request_email: str) -> str:
        email = account.get("email")
        self.__validate(email, request_email)
        self.__model.delete_account(email)
        return "Conta deletada com sucesso!"

    def __validate(self, email: str, request_email: str) -> None:
        if email != request_email:
            raise HttpUnauthorizedError("Email na solicitação não corresponde ao email nos cabeçalhos!")
        if not self.__model.check_account_exists(email):
            raise HttpNotFoundError("Email não existente no banco de dados!")
