from typing import Any

from log_formatter.base import LogFormatter
from service.core.request_data import RequestData
from service.core.response_data import ResponseData


class HTTPServiceFormatter(LogFormatter):
    def __init__(
            self,
            message,
            request: RequestData,
            response: ResponseData | None = None
    ):
        super(HTTPServiceFormatter, self).__init__(message=message)

        self.request: RequestData = request
        self.response: ResponseData = response or ResponseData()

        self.request_url: str = self.request.url
        self.request_method: str = self.request.method
        self.request_params: dict | None = self.request.params
        self.request_headers: dict | None = self.request.headers
        self.request_data: Any = self.request.data

        self.response_status: int = self.response.status
        self.response_data: dict | str | None = self.response.get_data()

        self.repr_fields = self.repr_fields + [
            'request_url',
            'request_method',
            'request_params',
            'request_headers',
            'request_data',

            'response_status',
            'response_data',
        ]
