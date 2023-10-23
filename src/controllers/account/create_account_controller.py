from src.models.interface.account_interface import AccountRepositoryInterface
from src.controllers.interface.account_controller_interface import ControllerInterface
from src.errors.types.http_not_found import HttpNotFoundError


class CreateAccountController(ControllerInterface):
    def __init__(self, model: AccountRepositoryInterface) -> None:
        self.__model = model

    def operate(self, account: dict) -> dict:
        self.__validate(account)
        self.__model.create_account(
            account.get("email"),
            account.get("senha"),
            account.get("saldo")
        )
        return self.__format_response(account)

    def __validate(self, account: dict) -> None:
        email = account.get("email")
        if self.__model.check_account_exists(email):
            raise HttpNotFoundError("Email já existente no banco de dados!")

    def __format_response(self, account: dict) -> dict:
        return {
            "status": "success",
            "data": account
        }