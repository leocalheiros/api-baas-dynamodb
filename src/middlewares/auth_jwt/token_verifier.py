from functools import wraps
from flask import jsonify, request
import jwt
from src.middlewares.auth_jwt.token_singleton import token_creator


def token_verify(function: callable) -> callable:

    @wraps(function)
    def decorated(*args, **kwargs):
        raw_token = request.headers.get('Authorization')
        email = request.headers.get('email')

        if not raw_token or not email:
            return jsonify({
                'errors': {
                    "detail": "Missing authorization",
                    "title": "MissingAuthorizationError"
                }
            }), 401
        try:
            token = raw_token.split()[1]
            token_information = jwt.decode(token, key=token_creator.get_token_key(), algorithms="HS256")
            token_email = token_information["email"]
        except jwt.InvalidSignatureError:
            return jsonify({
                'errors': {
                    "detail": "Invalid Token",
                    "title": "InvalidTokenError"
                }
            }), 401
        except jwt.ExpiredSignatureError:
            return jsonify({
                'errors': {
                    "detail": "Expired Token",
                    "title": "ExpiredTokenError"
                }
            }), 401
        except KeyError as e:
            return jsonify({
                'errors': {
                    "detail": "Invalid Token",
                    "title": "InvalidTokenError"
                }
            }), 401
        except jwt.exceptions.DecodeError:
            return jsonify({
                'errors': {
                    "detail": "Invalid Token",
                    "title": "InvalidTokenError"
                }
            }), 401
        if token_email != email:
            return jsonify({
                'errors': {
                    "detail": "User not authorized",
                    "title": "Unauthorized"
                }
            }), 401

        next_token = token_creator.refresh(token)

        return function(next_token, *args, **kwargs)

    return decorated
