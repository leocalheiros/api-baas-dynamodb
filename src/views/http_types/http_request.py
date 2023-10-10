from typing import Dict


class HttpRequest:
    def __init__(
        self,
        header: Dict = None,
        body: Dict = None,
        query_params: Dict = None,
        url: str = None,
        token_information: Dict = None
    ):
        self.header = header
        self.body = body
        self.query_params = query_params
        self.url = url
        self.token_information = token_information
