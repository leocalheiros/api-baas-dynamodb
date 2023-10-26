import boto3
from src.models.interface.credit_card_interface import CreditCardRepositoryInterface

ddb = boto3.resource('dynamodb')
table = ddb.Table('bank_table')


class CreditCardModel(CreditCardRepositoryInterface):
    def save_credit_card(self, email: str, card_data: dict) -> None:
        table.update_item(
            Key={'email': email},
            UpdateExpression="SET credit_card = :card_data",
            ExpressionAttributeValues={':card_data': card_data},
        )
