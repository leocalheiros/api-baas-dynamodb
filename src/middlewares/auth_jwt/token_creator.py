import jwt
from datetime import datetime, timedelta
import time


class TokenCreator:
    def __init__(self, token_key: str, exp_time_min: int, refresh_time_min: int):
        self.__TOKEN_KEY = token_key
        self.__EXP_TIME_MIN = exp_time_min
        self.__REFRESH_TIME_MIN = refresh_time_min

    def create(self, email: str):
        return self.__encode_token(email)

    def refresh(self, token: str):
        token_information = jwt.decode(token, key=self.__TOKEN_KEY, algorithms="HS256")
        token_email = token_information["email"]
        exp_time = token_information["exp"]

        if ((exp_time - time.time()) / 60) < self.__REFRESH_TIME_MIN:
            return self.__encode_token(token_email)

        return token

    def __encode_token(self, email: str):
        token = jwt.encode({
            'exp': datetime.utcnow() + timedelta(minutes=self.__EXP_TIME_MIN),
            'email': email
        }, key=self.__TOKEN_KEY, algorithm="HS256")

        return token

    def get_token_key(self):
        return self.__TOKEN_KEY
