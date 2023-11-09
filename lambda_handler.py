import awsgi
from flask import Flask
from src.main.routes import bank_blueprint
from src.main.routes import saldo_blueprint
from src.main.routes import pix_blueprint
from src.main.routes import payments_blueprint

app = Flask(__name__)
app.register_blueprint(bank_blueprint)
app.register_blueprint(saldo_blueprint)
app.register_blueprint(pix_blueprint)
app.register_blueprint(payments_blueprint)


def lambda_handler(event, context):
    return awsgi.response(app, event, context)
