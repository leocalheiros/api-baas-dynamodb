from src.models.interface.saldo_interface import SaldoRepositoryInterface
from src.models.interface.account_interface import AccountRepositoryInterface
from src.controllers.interface.saldo_controller_interface import SaldoControllerInterface
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_insufficient_balance_error import HttpInsufficientBalanceError


class DepositSaldoController(SaldoControllerInterface):
    def __init__(self, account_model: AccountRepositoryInterface, saldo_model: SaldoRepositoryInterface):
        self.__account_model = account_model
        self.__saldo_model = saldo_model

    def operate(self, email: str, amount: int) -> str:
        self.__validate(email, amount)
        self.__saldo_model.add_saldo(email, amount)
        return f"Depósito de {amount} realizado com sucesso na conta de {email}"

    def __validate(self, email: str, amount: int):
        if not self.__account_model.check_account_exists(email):
            raise HttpNotFoundError("Conta não existente no banco de dados")
        if amount <= 0:
            raise HttpInsufficientBalanceError("O valor do depósito deve ser maior que zero")
