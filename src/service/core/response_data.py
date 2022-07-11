from enum import Enum


class StatusCodes(Enum):
    HTTP_200 = 200
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_500 = 500


class ResponseData:
    def __init__(
            self,
            status: int = StatusCodes.HTTP_500.value,
            data: dict | str | None = None,
    ):
        self.status = status
        self._data = data if self.is_success_response() else None
        self._error = None if self.is_success_response() else data

    def is_success_response(self):
        return self.status in [StatusCodes.HTTP_200.value]

    def get_status(self) -> int:
        return self.status

    def get_data(self) -> dict | str:
        return self._data or self._error or {}

    def get_error(self) -> dict | str:
        return {} if self.is_success_response() else (self._error or {})
