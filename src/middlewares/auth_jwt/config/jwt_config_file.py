import os
from dotenv import load_dotenv
load_dotenv()

jwt_config = {
    "TOKEN_KEY": "1234",
    "EXP_TIME_MIN": 30,
    "REFRESH_TIME_MIN": 15
}
