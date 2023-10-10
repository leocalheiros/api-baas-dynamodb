from src.models.interface.account_interface import AccountRepositoryInterface
from src.controllers.interface.controller_interface import ControllerInterface
from src.errors.types.http_not_found import HttpNotFoundError


class GetAccountByEmailController(ControllerInterface):
    def __init__(self, model: AccountRepositoryInterface):
        self.__model = model

    def operate(self, email: str) -> str:
        self.__validate(email)
        conta = self.__model.get_account_by_email(email)
        return f'Conta encontrada: {conta}'

    def __validate(self, email: str):
        if not self.__model.check_account_exists(email):
            raise HttpNotFoundError('Conta não existente no banco de dados')
