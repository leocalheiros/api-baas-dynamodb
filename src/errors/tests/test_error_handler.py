import pytest
from src.errors.error_handler import handle_errors
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_bad_request import HttpBadRequest
from src.errors.types.http_insufficient_balance_error import HttpInsufficientBalanceError


def test_handle_errors_http_not_found():
    error = HttpNotFoundError("Resource not found")
    response = handle_errors(error)
    assert response.status_code == 404
    assert response.body == {
        "errors": [{
            "title": error.name,
            "detail": error.message
        }]
    }


def test_handle_errors_http_bad_request():
    error = HttpBadRequest("Bad request")
    response = handle_errors(error)
    assert response.status_code == 400
    assert response.body == {
        "errors": [{
            "title": error.name,
            "detail": error.message
        }]
    }


def test_handle_errors_http_unprocessable_entity():
    error = HttpUnprocessableEntityError("Unprocessable entity")
    response = handle_errors(error)
    assert response.status_code == 422
    assert response.body == {
        "errors": [{
            "title": error.name,
            "detail": error.message
        }]
    }


def test_handle_errors_insufficient_balance_error():
    error = HttpInsufficientBalanceError('InsufficientBalance')
    response = handle_errors(error)
    assert response.status_code == 400
    assert response.body == {
        "errors": [{
            "title": error.name,
            "detail": error.message
        }]
    }


def test_handle_errors_generic_error():
    error = Exception("Generic error")
    response = handle_errors(error)
    assert response.status_code == 500
    assert response.body == {
        "errors": [{
            "title": "Server Error",
            "detail": "Generic error"
        }]
    }
