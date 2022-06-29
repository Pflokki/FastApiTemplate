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


class RequestParameters:
    def __init__(
            self,
            url: str,
            params: dict | None,
            headers: dict | None,
            data: Any,
            _json: dict | None,
            auth: tuple[str, str] | None,
            timeout: int,
    ):
        self.url = url
        self.params = params
        self.headers = headers
        self.data = data
        self.json = _json
        self.auth = auth
        self.timeout = timeout

    def to_dict(self, exclude_none: bool = True) -> dict:
        params = dict(
            url=self.url,
            params=self.params,
            headers=self.headers,
            data=self.data,
            json=self.json,
            auth=self.auth,
            timeout=self.timeout,
        )
        if exclude_none:
            params = {k: v for k, v in params.items() if v}  # exclude None or empty values

        return params
