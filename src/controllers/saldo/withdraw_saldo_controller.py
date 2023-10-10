from src.models.interface.saldo_interface import SaldoRepositoryInterface
from src.models.interface.account_interface import AccountRepositoryInterface
from src.controllers.interface.saldo_controller_interface import SaldoControllerInterface
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_insufficient_balance_error import HttpInsufficientBalanceError


class WithdrawSaldoController(SaldoControllerInterface):
    def __init__(self, account_model: AccountRepositoryInterface, saldo_model: SaldoRepositoryInterface):
        self.__account_model = account_model
        self.__saldo_model = saldo_model

    def operate(self, email: str, amount: int) -> str:
        self.__validate(email, amount)
        self.__saldo_model.add_saldo(email, -amount)
        return f"Saque de {amount} realizado com sucesso na conta de {email}"

    def __validate(self, email: str, amount: int) -> None:
        if not self.__account_model.check_account_exists(email):
            raise HttpNotFoundError("Conta não existente no banco de dados")
        if not self.__check_saldo(email, amount):
            raise HttpInsufficientBalanceError("Saldo insuficiente na conta de origem")

    def __check_saldo(self, email: str, amount: int) -> bool:
        source_saldo = self.__saldo_model.check_saldo(email)
        return source_saldo >= amount
