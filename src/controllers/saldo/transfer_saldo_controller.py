from src.models.interface.saldo_interface import SaldoRepositoryInterface
from src.models.interface.account_interface import AccountRepositoryInterface
from src.controllers.interface.saldo_controller_interface import SaldoControllerInterface
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_insufficient_balance_error import HttpInsufficientBalanceError
from src.errors.types.http_unauthorized import HttpUnauthorizedError


class TransferSaldoController(SaldoControllerInterface):
    def __init__(self, account_model: AccountRepositoryInterface, saldo_model: SaldoRepositoryInterface):
        self.__account_model = account_model
        self.__saldo_model = saldo_model

    def operate(self, request_data: dict, request_email: str) -> str:
        source_email = request_data.get("source_email")
        target_email = request_data.get("target_email")
        amount = request_data.get("amount")
        self.__validate(source_email, target_email, amount, request_email)
        self.__saldo_model.add_saldo(target_email, amount)
        self.__saldo_model.add_saldo(source_email, -amount)
        return f"Transferência de {amount} realizada com sucesso da conta de {source_email} para {target_email}"

    def __validate(self, source_email: str, target_email: str, amount: int, request_email: str) -> None:
        if source_email != request_email:
            raise HttpUnauthorizedError("Email na solicitação não corresponde ao email nos cabeçalhos")
        if not self.__account_model.check_account_exists(source_email):
            raise HttpNotFoundError("Conta de origem não existente no banco de dados")
        if not self.__account_model.check_account_exists(target_email):
            raise HttpNotFoundError("Conta de destino não existente no banco de dados")
        if not self.__check_saldo(source_email, amount):
            raise HttpInsufficientBalanceError("Saldo insuficiente na conta de origem")

    def __check_saldo(self, email: str, amount: int) -> bool:
        source_saldo = self.__saldo_model.check_saldo(email)
        return source_saldo >= amount
