from src.views.account.get_account_by_email_view import GetAccountByEmailView
from src.controllers.account.get_account_by_email_controller import GetAccountByEmailController
from src.models.account_model import AccountModel


def get_account_by_email_composer(next_token=None):
    repo = AccountModel()
    controller = GetAccountByEmailController(repo)
    view = GetAccountByEmailView(controller)
    return view
