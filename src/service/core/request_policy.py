from settings import settings
from aiohttp.client_exceptions import (
    ClientConnectionError,
    ClientResponseError,
)


class RequestPolicy:
    def __init__(
            self,
            timeout: int = settings.BASE_SERVICE_TIMEOUT,
            retry_count: int = settings.BASE_SERVICE_RETRY_COUNT
    ):
        self.timeout: int = timeout
        self.retry_count: int = retry_count if retry_count >= 0 else 0

        self._retry_reason: list = [ClientConnectionError, ClientResponseError]
        self.retry_status_codes: list = []

    @property
    def retry_reason(self) -> tuple:
        return tuple(self._retry_reason)

    def is_need_retry(self, current_retry_count: int) -> bool:
        return self.retry_count > current_retry_count or (self.retry_count == 0 and current_retry_count == 0)

    def add_retry_reason(self, error: Exception) -> None:
        self._retry_reason.append(error)

    def add_retry_status_codes(self, codes: list) -> None:
        self.retry_status_codes.extend(codes)
