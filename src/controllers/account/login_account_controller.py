from src.models.interface.account_interface import AccountRepositoryInterface
from src.controllers.interface.account_controller_interface import ControllerInterface
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_unauthorized import HttpUnauthorizedError
from src.middlewares.auth_jwt.token_singleton import token_creator


class LoginAccountController(ControllerInterface):
    def __init__(self, model: AccountRepositoryInterface):
        self.__model = model

    def operate(self, email: str, senha: str) -> str:
        conta = self.__get_account(email)
        self.__validate(conta, senha)
        token = token_creator.create(email)
        return f'Login bem-sucedido: Seja bem-vindo, {email}. Seu token é: {token}'

    def __get_account(self, email: str):
        conta = self.__model.get_account_by_email(email)
        if conta is None:
            raise HttpNotFoundError('Conta não existente no banco de dados')
        return conta

    def __validate(self, conta, senha: str):
        if conta['senha'] != senha:
            raise HttpUnauthorizedError('Senha inválida!')
