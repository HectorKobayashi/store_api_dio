class BaseException(Exception):
    message: str = "Internal Server"

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message


class NotFoundException(BaseException):
    message = "Not found"

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message)
