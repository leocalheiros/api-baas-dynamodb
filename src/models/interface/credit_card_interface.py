from abc import ABC, abstractmethod


class CreditCardRepositoryInterface(ABC):
    @abstractmethod
    def save_credit_card(self, email: str, card_data: dict) -> None:
        pass

