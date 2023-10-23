from abc import ABC, abstractmethod


class PixControllerInterface:
    @abstractmethod
    def generate_payload(self, chavepix, valor, nome, cidade, txtId):
        pass
