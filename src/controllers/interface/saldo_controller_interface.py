from abc import ABC, abstractmethod


class SaldoControllerInterface(ABC):

    @abstractmethod
    def operate(self, request_data: dict, request_email: str) -> any:
        pass
