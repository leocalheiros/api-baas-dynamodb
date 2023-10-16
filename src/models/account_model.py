import boto3
from src.models.interface.account_interface import AccountRepositoryInterface

ddb = boto3.resource('dynamodb')
table = ddb.Table('bank_table')


class AccountModel(AccountRepositoryInterface):

    def create_account(self, email: str, senha: str, saldo: float) -> None:
            response = table.put_item(
                Item={
                    "email": email,
                    "senha": senha,
                    "saldo": saldo
                }
            )

    def delete_account(self, email: str) -> None:
        response = table.delete_item(
            Key={'email': email}
        )

    def get_account_by_email(self, email: str):
        response = table.get_item(Key={'email': email})

        if 'Item' in response:
            return response['Item']
        else:
            return None

    def check_account_exists(self, email: str) -> bool:
        response = table.get_item(
            Key={'email': email}
        )
        return 'Item' in response
