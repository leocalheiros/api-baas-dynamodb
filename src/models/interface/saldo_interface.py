from abc import ABC, abstractmethod


class SaldoRepositoryInterface(ABC):
    @abstractmethod
    def add_saldo(self, email: str, quantidade: int) -> None:
        pass

    @abstractmethod
    def update_saldo(self, email: str, novo_saldo: int) -> None:
        pass
