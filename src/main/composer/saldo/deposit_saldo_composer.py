from src.views.saldo.deposit_saldo_view import DepositView
from src.controllers.saldo.deposit_saldo_controller import DepositSaldoController
from src.models.saldo_model import SaldoModel
from src.models.account_model import AccountModel


def deposit_saldo_composer():
    repo1 = AccountModel()
    repo2 = SaldoModel()
    controller = DepositSaldoController(repo1, repo2)
    view = DepositView(controller)
    return view

