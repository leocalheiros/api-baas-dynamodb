from src.views.account.create_account_view import CreateAccountView
from src.controllers.account.create_account_controller import CreateAccountController
from src.models.account_model import AccountModel


def create_account_composer():
    repo = AccountModel()
    controller = CreateAccountController(repo)
    view = CreateAccountView(controller)
    return view
