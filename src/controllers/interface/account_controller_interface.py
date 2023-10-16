from abc import ABC, abstractmethod


class ControllerInterface(ABC):

    @abstractmethod
    def operate(self, account: dict, request_email: str) -> str:
        pass
