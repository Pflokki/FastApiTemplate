import aiohttp

from service.core.base import Base as BaseService
from service.core.request_policy import RequestPolicy
from service.core.request_parameters import RequestMethod


class ExampleServicePolicy(RequestPolicy):
    def __init__(self):
        super().__init__(timeout=5, retry_count=3)


class ExampleService(BaseService):
    def __init__(self):
        policy = ExampleServicePolicy()
        policy.add_retry_status_codes([500, 400])

        super().__init__(
            policy=policy,
        )

    @staticmethod
    async def loads_data(response: aiohttp.ClientResponse) -> str:
        return 'Hello, from ExampleService'

    async def get_alive_data(self):
        url: str = 'http://localhost:10500/live/'
        method: RequestMethod = RequestMethod.GET

        await self.send(
            url=url,
            method=method,
        )
        status, data = self.get_response_data()

        return status, data
