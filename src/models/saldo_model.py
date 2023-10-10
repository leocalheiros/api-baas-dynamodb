import boto3
from src.models.interface.saldo_interface import SaldoRepositoryInterface


ddb = boto3.resource('dynamodb')
table = ddb.Table('bank_table')


class SaldoModel(SaldoRepositoryInterface):
    def add_saldo(self, email: str, amount: int) -> None:
        table.update_item(
            Key={"email": email},
            UpdateExpression="SET saldo = if_not_exists(saldo, :start) + :amount",
            ExpressionAttributeValues={':start': 0, ':amount': amount}
        )

    def update_saldo(self, email: str, novo_saldo: int) -> None:
        table.update_item(
            Key={'email': email},
            UpdateExpression="SET saldo = :novo_saldo",
            ExpressionAttributeValues={':novo_saldo': novo_saldo}
        )

    def check_saldo(self, email: str) -> int:
        response = table.get_item(
            Key={'email': email}
        )
        if 'Item' in response:
            saldo = response['Item'].get('saldo', 0)
            return saldo
        return 0
