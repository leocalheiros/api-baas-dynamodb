from src.views.account.delete_account_view import DeleteAccountView
from src.controllers.account.delete_account_controller import DeleteAccountController
from src.models.account_model import AccountModel


def delete_account_composer(next_token=None):
    repo = AccountModel()
    controller = DeleteAccountController(repo)
    view = DeleteAccountView(controller)
    return view
