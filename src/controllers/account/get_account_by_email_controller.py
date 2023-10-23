from src.models.interface.account_interface import AccountRepositoryInterface
from src.controllers.interface.account_controller_interface import ControllerInterface
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_unauthorized import HttpUnauthorizedError


class GetAccountByEmailController(ControllerInterface):
    def __init__(self, model: AccountRepositoryInterface):
        self.__model = model

    def operate(self, account: dict, request_email: str) -> dict:
        email = account.get("email")
        self.__validate(email, request_email)
        conta = self.__model.get_account_by_email(email)
        return self.__format_response(conta)

    def __validate(self, email: str, request_email: str):
        if email != request_email:
            raise HttpUnauthorizedError("Email na solicitação não corresponde ao email nos cabeçalhos!")
        if not self.__model.check_account_exists(email):
            raise HttpNotFoundError('Conta não existente no banco de dados')

    def __format_response(self, conta: dict) -> dict:
        return {
            "message": "success",
            "data": conta
        }
