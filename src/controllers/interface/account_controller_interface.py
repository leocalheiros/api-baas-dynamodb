from abc import ABC, abstractmethod


class ControllerInterface(ABC):

    @abstractmethod
    def operate(self, account: dict) -> any:
        pass
