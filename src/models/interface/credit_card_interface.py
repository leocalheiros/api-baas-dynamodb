from abc import ABC, abstractmethod


class CreditCardRepositoryInterface(ABC):
    @abstractmethod
    def save_credit_card(self, email: str, card_data: dict) -> None:
        pass

    @abstractmethod
    def get_credit_card(self, email: str):
        pass

    @abstractmethod
    def delete_credit_card(self, email: str) -> None:
        pass
