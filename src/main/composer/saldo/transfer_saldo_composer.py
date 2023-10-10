from src.views.saldo.transfer_saldo_view import TransferView
from src.controllers.saldo.transfer_saldo_controller import TransferSaldoController
from src.models.saldo_model import SaldoModel
from src.models.account_model import AccountModel


def transfer_saldo_composer():
    repo1 = AccountModel()
    repo2 = SaldoModel()
    controller = TransferSaldoController(repo1, repo2)
    view = TransferView(controller)
    return view

