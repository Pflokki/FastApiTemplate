import json
import aiohttp
from aiohttp.client_exceptions import ClientResponseError

from service.core.exceptions import ServiceUnavailable
from service.core.request_paginator.base_paginator import Paginator
from service.core.request_policy import RequestPolicy
from service.core.request_data import RequestData
from service.core.response_data import ResponseData

from service.core.base_service_logger_mixin import BaseServiceLoggerMixin


class Base(BaseServiceLoggerMixin):
    def __init__(
            self,
            auth: tuple[str, str] | None = None,
            policy: RequestPolicy = None
    ):
        self.policy: RequestPolicy = policy or RequestPolicy()
        self.auth: tuple[str, str] | None = auth

        self._request_history: list[tuple[RequestData, ResponseData]] = []

    def _add_history(self, request: RequestData, response: ResponseData):
        self._request_history.append((request, response))

    def _clear_history(self):
        self._request_history.clear()

    def get_response(self) -> ResponseData:
        if self._request_history:
            last_history: tuple[RequestData, ResponseData] | None = self._request_history[-1]
            last_request = last_history[1] if last_history else ResponseData()
        else:
            last_request = ResponseData()

        return last_request

    async def loads_data(self, response: aiohttp.ClientResponse) -> dict | str:
        data = await response.text()
        try:
            return json.loads(data)
        except json.JSONDecodeError as error:
            self._log_representation_exception(error)
            return data

    async def _send_request(
            self,
            session: aiohttp.ClientSession,
            request_data: RequestData,
            request_policy: RequestPolicy
    ) -> ResponseData:
        async with getattr(session, request_data.method)(
                **request_data.to_dict(), timeout=request_policy.timeout
        ) as response:
            return ResponseData(response.status, await self.loads_data(response))

    async def send(
            self,
            request_data: RequestData,
            request_policy: RequestPolicy = None,
            session: aiohttp.ClientSession = None,
            is_need_close_session: bool = True,
    ) -> None:
        is_need_close_session: bool = session is not None and is_need_close_session
        session: aiohttp.ClientSession = session or aiohttp.ClientSession()
        request_policy: RequestPolicy = request_policy or self.policy

        response_data = None
        retry_count = 0
        while request_policy.is_need_retry(retry_count):
            try:

                self._log_request(request_data)

                response_data = await self._send_request(session, request_data, request_policy)
                self._add_history(request_data, response_data)

                self._log_response(request_data, response_data)

                if response_data.status in self.policy.retry_status_codes:
                    raise ClientResponseError

                break

            except self.policy.retry_reason as error:
                retry_count += 1
                self._log_retry_exception(error, request_data, self.policy.retry_count - retry_count)
            except Exception as error:
                self._log_base_send_request_exception(error, request_data)
                break

        if is_need_close_session:
            await session.close()

        if not response_data:
            raise ServiceUnavailable

    async def paginate(
            self,
            paginator: Paginator,
            request_policy: RequestPolicy = None,
            session: aiohttp.ClientSession = None,
    ) -> None:
        self._clear_history()

        session: aiohttp.ClientSession = session or aiohttp.ClientSession()

        for request_data in paginator.get_paginated_request():
            try:
                await self.send(request_data, request_policy, session, is_need_close_session=False)
            except ServiceUnavailable:
                pass

        await session.close()
