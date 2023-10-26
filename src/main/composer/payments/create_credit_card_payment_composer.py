from src.views.payments.create_credit_card_payment_view import CreateCreditCardPaymentView
from src.controllers.payments.create_credit_card_payment_controller import TransactionController
from src.models.account_model import AccountModel
from src.models.credit_card_model import CreditCardModel


def create_credit_card_payment_composer(next_token=None):
    repo1 = AccountModel()
    repo2 = CreditCardModel()
    controller = TransactionController(repo1, repo2)
    view = CreateCreditCardPaymentView(controller)
    return view
