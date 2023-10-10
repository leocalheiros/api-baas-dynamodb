class HttpResponse:

    def __init__(self, status_code: int, body: any):
        self.status_code = status_code
        self.body = body
