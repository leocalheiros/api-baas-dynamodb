from ..views.http_types.http_response import HttpResponse
from .types.http_not_found import HttpNotFoundError
from .types.http_unprocessable_entity import HttpUnprocessableEntityError
from .types.http_bad_request import HttpBadRequest
from .types.http_unauthorized import HttpUnauthorizedError
from .types.http_insufficient_balance_error import HttpInsufficientBalanceError


def handle_errors(error: Exception) -> HttpResponse:
    if isinstance(error, (HttpNotFoundError, HttpUnprocessableEntityError, HttpBadRequest, HttpUnauthorizedError, HttpInsufficientBalanceError)):
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors": [{
                    "title": error.name,
                    "detail": error.message
                }]
            }
        )

    return HttpResponse(
        status_code=500,
        body={
            "errors": [{
                "title": "Server Error",
                "detail": str(error)
            }]
        }
    )
