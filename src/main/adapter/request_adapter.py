from typing import Type
from flask import request as FlaskRequest
from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse
from src.views.interface.views_interface import ViewInterface


def request_adapter(request: FlaskRequest, callback: Type[ViewInterface]) -> HttpResponse:
    http_request = HttpRequest(
        header=request.headers,
        body=request.json,
        query_params=request.args,
        url=request.full_path,
    )

    http_response = callback.handle(http_request)
    return http_response
