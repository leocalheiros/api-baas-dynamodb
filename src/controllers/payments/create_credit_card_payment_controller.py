import base64
from src.controllers.interface.account_controller_interface import ControllerInterface
from src.models.interface.account_interface import AccountRepositoryInterface
from src.models.interface.credit_card_interface import CreditCardRepositoryInterface
from src.errors.types.http_unauthorized import HttpUnauthorizedError
from src.errors.types.http_not_found import HttpNotFoundError


class TransactionController(ControllerInterface):
    def __init__(self, account_model: AccountRepositoryInterface, card_model: CreditCardRepositoryInterface):
        self.__account_model = account_model
        self.__card_model = card_model

    def operate(self, request_data: dict, request_email: str) -> dict:
        email = request_data.get('email')
        amount = request_data.get('amount')

        card_data = self.__card_model.get_credit_card(email)
        self.__validate(email, request_email, amount, card_data)

        decoded_card_number = self.__decode_card_number(card_data.get("card_number"))

        # Add transaction process here

        return {"status": "success", "email": email, "amount": amount, "card_number": decoded_card_number}

    def __validate(self, email: str, request_email: str, amount: float, card_data: dict):
        if email != request_email:
            raise HttpUnauthorizedError("Email na solicitação não corresponde ao email nos cabeçalhos!")
        if not self.__account_model.check_account_exists(email):
            raise HttpNotFoundError("Conta não existente no banco de dados")
        if not card_data:
            raise HttpNotFoundError("Usuário não possui informações de cartão de crédito na base de dados")

    def __decode_card_number(self, encoded_card_number: str) -> str:
        decoded_bytes = base64.b64decode(encoded_card_number.encode())
        return decoded_bytes.decode()
