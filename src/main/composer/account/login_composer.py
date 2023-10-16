from src.views.account.login_view import LoginAccountView
from src.controllers.account.login_account_controller import LoginAccountController
from src.models.account_model import AccountModel


def login_composer():
    repo = AccountModel()
    controller = LoginAccountController(repo)
    view = LoginAccountView(controller)
    return view
