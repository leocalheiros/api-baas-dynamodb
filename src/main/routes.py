from flask import Blueprint, request, jsonify
from src.main.composer.account.create_account_composer import create_account_composer
from src.main.composer.account.delete_account_composer import delete_account_composer
from src.main.composer.account.get_account_by_email_composer import get_account_by_email_composer
from src.main.composer.saldo.deposit_saldo_composer import deposit_saldo_composer
from src.main.composer.saldo.transfer_saldo_composer import transfer_saldo_composer
from src.main.composer.saldo.withdraw_saldo_composer import withdraw_saldo_composer
from src.main.adapter.request_adapter import request_adapter


bank_blueprint = Blueprint('bank', __name__)
saldo_blueprint = Blueprint('saldo', __name__)

@bank_blueprint.route('/create-person', methods=['POST'])
def create_person():
    http_response = request_adapter(request, create_account_composer())
    return jsonify(http_response.body, http_response.status_code)


@bank_blueprint.route('/delete-person', methods=['DELETE'])
def delete_person():
    http_response = request_adapter(request, delete_account_composer())
    return jsonify(http_response.body, http_response.status_code)


@bank_blueprint.route('/get-person', methods=['POST'])
def get_person():
    http_response = request_adapter(request, get_account_by_email_composer())
    return jsonify(http_response.body, http_response.status_code)


@saldo_blueprint.route('/deposit-saldo', methods=['POST'])
def deposit_saldo():
    http_response = request_adapter(request, deposit_saldo_composer())
    return jsonify(http_response.body, http_response.status_code)


@saldo_blueprint.route('/transfer-saldo', methods=['POST'])
def transfer_saldo():
    http_response = request_adapter(request, transfer_saldo_composer())
    return jsonify(http_response.body, http_response.status_code)


@saldo_blueprint.route('/withdraw-saldo', methods=['POST'])
def withdraw_saldo():
    http_response = request_adapter(request, withdraw_saldo_composer())
    return jsonify(http_response.body, http_response.status_code)


@bank_blueprint.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "sucesso!"})
