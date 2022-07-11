from typing import Any
from enum import Enum


class RequestMethod(Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'
    OPTIONS = 'options'
    HEAD = 'head'


class RequestData:
    def __init__(
            self,
            url: str,
            method: str,
            params: dict | None = None,
            headers: dict | None = None,
            data: Any = None,
            auth: tuple[str, str] | None = None,
    ):
        self.url = url
        self.method = method
        self.params = params
        self.headers = headers
        self.json, self.data = self.parse_data(data)
        self.auth = auth

    @staticmethod
    def parse_data(data: dict | Any) -> tuple[dict | None, Any]:
        _json: dict | None = data if isinstance(data, dict) else None
        data: Any = data if not isinstance(data, dict) else None
        return _json, data

    def to_dict(self, exclude_none: bool = True) -> dict:
        params = dict(
            url=self.url,
            params=self.params,
            headers=self.headers,
            data=self.data,
            json=self.json,
            auth=self.auth,
        )
        if exclude_none:
            params = {k: v for k, v in params.items() if v}  # exclude None or empty values

        return params
