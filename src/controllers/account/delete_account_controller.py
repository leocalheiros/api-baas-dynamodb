from src.models.interface.account_interface import AccountRepositoryInterface
from src.controllers.interface.controller_interface import ControllerInterface
from src.errors.types.http_not_found import HttpNotFoundError


class DeleteAccountController(ControllerInterface):
    def __init__(self, model: AccountRepositoryInterface):
        self.__model = model

    def operate(self, account: dict) -> str:
        email = account.get("email")
        self.__validate(email)
        self.__model.delete_account(email)
        return "Conta deletada com sucesso!"

    def __validate(self, email: str) -> None:
        if not self.__model.check_account_exists(email):
            raise HttpNotFoundError("Email não existente no banco de dados!")
