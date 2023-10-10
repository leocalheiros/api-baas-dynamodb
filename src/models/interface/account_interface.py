from abc import ABC, abstractmethod


class AccountRepositoryInterface(ABC):
    @abstractmethod
    def create_account(self, email: str, senha: str, saldo: float) -> None:
        pass

    @abstractmethod
    def delete_account(self, email: str) -> None:
        pass

    @abstractmethod
    def get_account_by_email(self, email: str) -> None:
        pass

    @abstractmethod
    def check_account_exists(self, email: str) -> bool:
        pass
