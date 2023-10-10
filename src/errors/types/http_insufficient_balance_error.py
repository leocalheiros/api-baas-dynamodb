class HttpInsufficientBalanceError(Exception):

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.name = 'InsufficientBalanceError'
        self.status_code = 400
