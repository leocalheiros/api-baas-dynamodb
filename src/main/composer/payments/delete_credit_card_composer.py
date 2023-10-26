from src.views.payments.delete_credit_card_view import DeleteCreditCardView
from src.controllers.payments.delete_credit_card_controller import DeleteCreditCardController
from src.models.account_model import AccountModel
from src.models.credit_card_model import CreditCardModel


def delete_credit_card_composer(next_token=None):
    repo1 = AccountModel()
    repo2 = CreditCardModel()
    controller = DeleteCreditCardController(repo1, repo2)
    view = DeleteCreditCardView(controller)
    return view
