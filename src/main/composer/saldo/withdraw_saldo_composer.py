from src.views.saldo.withdraw_saldo_view import WithdrawView
from src.controllers.saldo.withdraw_saldo_controller import WithdrawSaldoController
from src.models.saldo_model import SaldoModel
from src.models.account_model import AccountModel


def withdraw_saldo_composer():
    repo1 = AccountModel()
    repo2 = SaldoModel()
    controller = WithdrawSaldoController(repo1, repo2)
    view = WithdrawView(controller)
    return view
