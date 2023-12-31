from flask import Blueprint, request, jsonify
from src.main.composer.account.create_account_composer import create_account_composer
from src.main.composer.account.delete_account_composer import delete_account_composer
from src.main.composer.account.get_account_by_email_composer import get_account_by_email_composer
from src.main.composer.account.login_composer import login_composer
from src.main.composer.saldo.deposit_saldo_composer import deposit_saldo_composer
from src.main.composer.saldo.transfer_saldo_composer import transfer_saldo_composer
from src.main.composer.saldo.withdraw_saldo_composer import withdraw_saldo_composer
from src.main.composer.pix.pix_composer import pix_composer
from src.main.composer.payments.register_credit_card_composer import register_credit_card_composer
from src.main.composer.payments.create_credit_card_payment_composer import create_credit_card_payment_composer
from src.main.composer.payments.delete_credit_card_composer import delete_credit_card_composer
from src.main.adapter.request_adapter import request_adapter
from src.middlewares.auth_jwt.token_verifier import token_verify

bank_blueprint = Blueprint('bank', __name__)
saldo_blueprint = Blueprint('saldo', __name__)
pix_blueprint = Blueprint('pix', __name__)
payments_blueprint = Blueprint('payments', __name__)


@bank_blueprint.route('/create-person', methods=['POST'])
def create_person():
    http_response = request_adapter(request, create_account_composer())
    return jsonify(http_response.body), http_response.status_code


@bank_blueprint.route('/delete-person', methods=['DELETE'])
@token_verify
def delete_person(next_token):
    http_response = request_adapter(request, delete_account_composer(next_token=next_token))
    return jsonify(http_response.body), http_response.status_code


@bank_blueprint.route('/get-person', methods=['POST'])
@token_verify
def get_person(next_token):
    http_response = request_adapter(request, get_account_by_email_composer(next_token=next_token))
    return jsonify(http_response.body), http_response.status_code


@bank_blueprint.route('/login', methods=['POST'])
def login():
    http_response = request_adapter(request, login_composer())
    return jsonify(http_response.body), http_response.status_code


@saldo_blueprint.route('/deposit-saldo', methods=['POST'])
@token_verify
def deposit_saldo(next_token):
    http_response = request_adapter(request, deposit_saldo_composer(next_token=next_token))
    return jsonify(http_response.body), http_response.status_code


@saldo_blueprint.route('/transfer-saldo', methods=['POST'])
@token_verify
def transfer_saldo(next_token):
    http_response = request_adapter(request, transfer_saldo_composer(next_token=next_token))
    return jsonify(http_response.body), http_response.status_code


@saldo_blueprint.route('/withdraw-saldo', methods=['POST'])
@token_verify
def withdraw_saldo(next_token):
    http_response = request_adapter(request, withdraw_saldo_composer(next_token=next_token))
    return jsonify(http_response.body), http_response.status_code


@pix_blueprint.route('/gerar-pix', methods=['POST'])
def gerar_pix():
    http_response = request_adapter(request, pix_composer())
    return jsonify(http_response.body), http_response.status_code


@payments_blueprint.route('/register-credit-card', methods=['POST'])
@token_verify
def register_credit_card(next_token):
    http_response = request_adapter(request, register_credit_card_composer(next_token=next_token))
    return jsonify(http_response.body), http_response.status_code


@payments_blueprint.route('/create-payment', methods=['POST'])
@token_verify
def create_credit_card_payment(next_token):
    http_response = request_adapter(request, create_credit_card_payment_composer(next_token=next_token))
    return jsonify(http_response.body), http_response.status_code


@payments_blueprint.route('/delete-card', methods=['POST'])
@token_verify
def delete_credit_card(next_token):
    http_response = request_adapter(request, delete_credit_card_composer(next_token=next_token))
    return jsonify(http_response.body), http_response.status_code


@bank_blueprint.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "sucesso!"})
