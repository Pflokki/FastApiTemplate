import aiohttp

from service.core.base import Base as BaseService
from service.core.request_policy import RequestPolicy
from service.core.request_data import RequestData, RequestMethod


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
        request_data = RequestData(
            'http://localhost:10500/live/',
            RequestMethod.GET.value,
        )

        await self.send(request_data)

        response = self.get_response()

        return response.status, response.get_data()
