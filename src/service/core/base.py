from typing import Any
import json
import aiohttp
from aiohttp.client_exceptions import ClientResponseError

from service.core.exceptions import ServiceUnavailable
from service.core.request_policy import RequestPolicy
from service.core.request_parameters import RequestParameters, RequestMethod
from settings import get_logger


logger = get_logger('http_service')


class Base:
    def __init__(
            self,
            auth: tuple[str, str] | None = None,
            policy: RequestPolicy = None
    ):
        self.policy: RequestPolicy = policy or RequestPolicy()
        self.auth: tuple[str, str] | None = auth

        self._request_history: list[tuple[RequestParameters, aiohttp.ClientResponse]] = []

    def _add_history(self, request_parameters: RequestParameters, response: aiohttp.ClientResponse):
        self._request_history.append((request_parameters, response))

    def get_response(self) -> aiohttp.ClientResponse | None:
        ''' Use response.loaded_data for getting data '''

        last_request = self._request_history[-1]
        return last_request[1] if last_request else None

    def get_response_data(self) -> tuple[int | None, dict | str | None]:
        response: aiohttp.ClientResponse | None = self.get_response()

        status, data = None, None
        if response:
            status = response.status
            data = response.loaded_data  # custom field from self.send(...)

        return status, data

    @staticmethod
    def parse_data(data: dict | Any) -> tuple[dict | None, Any]:
        _json: dict | None = data if isinstance(data, dict) else None
        data: Any = data if not isinstance(data, dict) else None
        return _json, data

    @staticmethod
    async def loads_data(response: aiohttp.ClientResponse) -> dict | str:
        data = await response.text()
        try:
            return json.loads(data)
        except json.JSONDecodeError as error:
            logger.error(f'Error while decode data from response | {error}')
            return data

    async def send(
            self,
            url: str,
            method: RequestMethod,
            headers: dict | None = None,
            params: dict | None = None,
            data: dict | Any = None,
            policy: RequestPolicy = None,
            session: aiohttp.ClientSession = None,
    ) -> None:
        _json, data = self.parse_data(data)
        policy: RequestPolicy = policy or self.policy

        request_parameters = RequestParameters(
            url=url,
            params=params,
            headers=headers,
            data=data,
            _json=_json,
            auth=self.auth,
            timeout=policy.timeout,
        )

        status = None
        retry_count: int = self.policy.retry_count
        is_need_close_session: bool = session is None
        session: aiohttp.ClientSession = session or aiohttp.ClientSession()
        while retry_count >= 0:
            try:
                logger.info(f'Request to {url} sent')
                async with getattr(session, method.value)(**request_parameters.to_dict()) as response:
                    status = response.status
                    logger.info(f'Response from {url} received | {status}')

                    # store data to response.loaded_data, because data erased after connection closed
                    response.loaded_data = await self.loads_data(response)

                    if status in self.policy.retry_status_codes:
                        raise ClientResponseError
                    break
            except self.policy.retry_reason as error:
                logger.warning(
                    f'Warning, error {type(error)} while sending request to {url}, '
                    f'retry count {self.policy.retry_count - retry_count + 1}...'
                )
                retry_count -= 1
            except Exception as error:
                logger.error(f'Error {type(error)} while sending request to {url}')
                break
            else:
                retry_count -= 1

        if is_need_close_session:
            await session.close()

        if status is None:
            raise ServiceUnavailable

        self._add_history(request_parameters, response)
