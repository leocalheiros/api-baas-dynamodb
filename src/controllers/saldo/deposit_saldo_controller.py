from src.models.interface.saldo_interface import SaldoRepositoryInterface
from src.models.interface.account_interface import AccountRepositoryInterface
from src.controllers.interface.saldo_controller_interface import SaldoControllerInterface
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_unauthorized import HttpUnauthorizedError


class DepositSaldoController(SaldoControllerInterface):
    def __init__(self, account_model: AccountRepositoryInterface, saldo_model: SaldoRepositoryInterface):
        self.__account_model = account_model
        self.__saldo_model = saldo_model

    def operate(self, request_data: dict, request_email: str) -> str:
        email = request_data.get('email')
        amount = request_data.get('amount')
        self.__validate(email, request_email)
        self.__saldo_model.add_saldo(email, amount)
        return f"Depósito de {amount} realizado com sucesso na conta de {email}"

    def __validate(self, email: str, request_email: str):
        if email != request_email:
            raise HttpUnauthorizedError("Email na solicitação não corresponde ao email nos cabeçalhos!")
        if not self.__account_model.check_account_exists(email):
            raise HttpNotFoundError("Conta não existente no banco de dados")
