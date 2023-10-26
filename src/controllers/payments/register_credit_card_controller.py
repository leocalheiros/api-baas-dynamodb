from src.controllers.interface.account_controller_interface import ControllerInterface
from src.models.interface.account_interface import AccountRepositoryInterface
from src.models.interface.credit_card_interface import CreditCardRepositoryInterface
from src.errors.types.http_unauthorized import HttpUnauthorizedError
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_bad_request import HttpBadRequest
import base64
import re
import datetime


class RegisterCardController(ControllerInterface):
    def __init__(self, account_model: AccountRepositoryInterface, card_model: CreditCardRepositoryInterface):
        self.__account_model = account_model
        self.__card_model = card_model

    def operate(self, request_data: dict, request_email: str) -> dict:
        email = request_data.get('email')
        card_number = request_data.get('card_number')
        expiration_month = request_data.get('expiration_month')
        expiration_year = request_data.get('expiration_year')
        security_code = request_data.get('security_code')
        holder_name = request_data.get('holder_name')

        self.__validate(email, request_email, card_number, security_code, expiration_month, expiration_year)

        encoded_card_number = self.__encode_card_number(card_number)

        card_data = {
            "card_number": encoded_card_number,
            "expiration_month": expiration_month,
            "expiration_year": expiration_year,
            "security_code": security_code,
            "holder_name": holder_name
        }

        self.__card_model.save_credit_card(email, card_data)

        return self.__format_response(email)

    def __validate(self, email: str, request_email: str, card_number: str, security_code: int, expiration_month: int,
                   expiration_year: int):
        if email != request_email:
            raise HttpUnauthorizedError("Email na solicitação não corresponde ao email nos cabeçalhos!")
        if not self.__account_model.check_account_exists(email):
            raise HttpNotFoundError("Conta não existente no banco de dados")
        if not self.__is_valid_credit_card_number(card_number):
            raise HttpBadRequest("Número de cartão de crédito inválido")
        if not self.__is_valid_security_code(security_code):
            raise HttpBadRequest("Código de segurança (CVV) inválido")
        if not self.__is_valid_expiration_date(expiration_month, expiration_year):
            raise HttpBadRequest("Data de expiração inválida")

    def __encode_card_number(self, card_number: str) -> str:
        encoded_bytes = base64.b64encode(card_number.encode())
        return encoded_bytes.decode()

    def __is_valid_credit_card_number(self, card_number: str) -> bool:
        card_number = re.sub(r'\D', '', card_number)

        if not (13 <= len(card_number) <= 19):
            return False

        # Luhn algorithm
        digits = [int(digit) for digit in card_number]
        checksum = 0

        for i in range(len(digits) - 2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9

        checksum = sum(digits) % 10

        return checksum == 0

    def __is_valid_security_code(self, security_code: int) -> bool:
        return re.match(r'^\d{3,4}$', str(security_code)) is not None

    def __is_valid_expiration_date(self, expiration_month: int, expiration_year: int):
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month

        if (
                expiration_month < 1 or
                expiration_month > 12 or
                (expiration_year < current_year) or
                (expiration_year == current_year and expiration_month < current_month)
        ):
            return False

        return True

    def __format_response(self, email: str) -> dict:
        return {
            "data": {
                "status": "success",
                "email": email
            }
        }
