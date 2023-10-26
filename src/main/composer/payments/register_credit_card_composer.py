from src.views.payments.register_credit_card_view import RegisterCardView
from src.controllers.payments.register_credit_card_controller import RegisterCardController
from src.models.account_model import AccountModel
from src.models.credit_card_model import CreditCardModel


def register_credit_card_composer(next_token=None):
    repo1 = AccountModel()
    repo2 = CreditCardModel()
    controller = RegisterCardController(repo1, repo2)
    view = RegisterCardView(controller)
    return view
