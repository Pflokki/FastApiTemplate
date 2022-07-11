import json
import aiohttp
from aiohttp.client_exceptions import ClientResponseError

from service.core.exceptions import ServiceUnavailable
from service.core.request_policy import RequestPolicy
from service.core.request_data import RequestData
from service.core.response_data import ResponseData
from log_formatter.http_service_formatter import HTTPServiceFormatter, LogFormatter
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

        self._request_history: list[tuple[RequestData, ResponseData]] = []

    def _add_history(self, request: RequestData, response: ResponseData):
        self._request_history.append((request, response))

    def get_response(self) -> ResponseData:
        last_request: tuple[RequestData, ResponseData] | None = self._request_history[-1]
        return last_request[1] if last_request else ResponseData()

    @staticmethod
    async def loads_data(response: aiohttp.ClientResponse) -> dict | str:
        data = await response.text()
        try:
            return json.loads(data)
        except json.JSONDecodeError as error:
            log_data = LogFormatter(f'Error while decode data from response | {error}')
            logger.error(log_data.get_str_record())
            return data

    async def send(
            self,
            request_data: RequestData,
            policy: RequestPolicy = None,
            session: aiohttp.ClientSession = None,
    ) -> None:
        is_need_close_session: bool = session is None
        session: aiohttp.ClientSession = session or aiohttp.ClientSession()
        policy: RequestPolicy = policy or self.policy

        status = None
        retry_count: int = self.policy.retry_count
        while retry_count >= 0:
            try:

                log_data = HTTPServiceFormatter(
                    message='Sending request',
                    request=request_data,
                )
                logger.info(log_data.get_str_record())

                async with getattr(session, request_data.method)(
                        **request_data.to_dict(), timeout=policy.timeout
                ) as response:
                    status = response.status
                    response_data = ResponseData(response.status, await self.loads_data(response))

                    log_data = HTTPServiceFormatter(
                        message='Response received',
                        request=request_data,
                        response=response_data,
                    )
                    logger.info(log_data.get_str_record())

                    if response_data.status in self.policy.retry_status_codes:
                        raise ClientResponseError

                    self._add_history(request_data, response_data)
                    retry_count = -1

            except self.policy.retry_reason as error:
                retry_count -= 1
                log_data = HTTPServiceFormatter(
                    message=f'Warning, error {type(error)} while sending request, '
                            f'retry count {self.policy.retry_count - retry_count}...',
                    request=request_data,
                )
                logger.info(log_data.get_str_record())

            except Exception as error:
                log_data = HTTPServiceFormatter(
                    message=f'Error {type(error)} while sending request',
                    request=request_data,
                )
                logger.info(log_data.get_str_record())
                break
            else:
                retry_count -= 1

        if is_need_close_session:
            await session.close()

        if status is None:
            raise ServiceUnavailable
