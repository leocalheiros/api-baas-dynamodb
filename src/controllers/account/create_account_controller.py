from src.models.interface.account_interface import AccountRepositoryInterface
from src.controllers.interface.controller_interface import ControllerInterface
from src.errors.types.http_not_found import HttpNotFoundError


class CreateAccountController(ControllerInterface):
    def __init__(self, model: AccountRepositoryInterface) -> None:
        self.__model = model

    def operate(self, account: dict) -> str:
        self.__validate(account)
        self.__model.create_account(
            account.get("email"),
            account.get("senha"),
            account.get("saldo")
        )
        return "Usuário criado com sucesso! Utilize seus dados inputados para fazer operações!"

    def __validate(self, account: dict) -> None:
        email = account.get("email")
        if self.__model.check_account_exists(email):
            raise HttpNotFoundError("Email já existente no banco de dados!")
