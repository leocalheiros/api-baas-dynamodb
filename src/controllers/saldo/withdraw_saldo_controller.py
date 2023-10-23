from src.models.interface.saldo_interface import SaldoRepositoryInterface
from src.models.interface.account_interface import AccountRepositoryInterface
from src.controllers.interface.saldo_controller_interface import SaldoControllerInterface
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_insufficient_balance_error import HttpInsufficientBalanceError
from src.errors.types.http_unauthorized import HttpUnauthorizedError


class WithdrawSaldoController(SaldoControllerInterface):
    def __init__(self, account_model: AccountRepositoryInterface, saldo_model: SaldoRepositoryInterface):
        self.__account_model = account_model
        self.__saldo_model = saldo_model

    def operate(self, request_data: dict, request_email: str) -> dict:
        email = request_data.get("email")
        amount = request_data.get("amount")
        self.__validate(email, amount, request_email)
        self.__saldo_model.add_saldo(email, -amount)
        return self.__format_response(email, amount)

    def __validate(self, email: str, amount: int, request_email: str) -> None:
        if email != request_email:
            raise HttpUnauthorizedError("Email na solicitação não corresponde ao email nos cabeçalhos!")
        if not self.__account_model.check_account_exists(email):
            raise HttpNotFoundError("Conta não existente no banco de dados")
        if not self.__check_saldo(email, amount):
            raise HttpInsufficientBalanceError("Saldo insuficiente na conta de origem")

    def __check_saldo(self, email: str, amount: int) -> bool:
        source_saldo = self.__saldo_model.check_saldo(email)
        return source_saldo >= amount

    def __format_response(self, email: str, amount: int) -> dict:
        return {
            "data": {
                "status": "success",
                "amount": amount,
                "email": email
            }
        }
