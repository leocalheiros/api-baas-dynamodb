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
                'error': 'Não autorizado, por favor insira os headers necessários'
            }), 401
        try:
            token = raw_token.split()[1]
            token_information = jwt.decode(token, key=token_creator.get_token_key(), algorithms="HS256")
            token_email = token_information["email"]
        except jwt.InvalidSignatureError:
            return jsonify({
                'error': 'Token inválido'
            }), 401
        except jwt.ExpiredSignatureError:
            return jsonify({
                'error': 'Token expirado'
            }), 401
        except KeyError as e:
            return jsonify({
                'error': 'Token inválido'
            }), 401
        except jwt.exceptions.DecodeError:
            return jsonify({
                'error': 'Token inválido!'
            }), 401
        if token_email != email:
            return jsonify({
                'error': 'User não permitido'
            }), 401

        next_token = token_creator.refresh(token)

        return function(next_token, *args, **kwargs)

    return decorated
