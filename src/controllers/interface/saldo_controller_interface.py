from abc import ABC, abstractmethod


class SaldoControllerInterface(ABC):

    @abstractmethod
    def operate(self, email: str, quantidade: int) -> str:
        pass
