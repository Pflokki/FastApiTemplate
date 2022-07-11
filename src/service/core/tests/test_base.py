import pytest
from unittest.mock import AsyncMock

from service.core.base import Base
from service.core.request_data import RequestData, RequestMethod
from service.core.request_policy import RequestPolicy


class TestBaseService:
    @pytest.fixture(scope='class')
    def base_service(self):
        rp = RequestPolicy(timeout=5, retry_count=0)
        return Base(policy=rp)

    @pytest.fixture(scope='class')
    def request_data(self):
        return RequestData(
            'https://google.com/',
            RequestMethod.GET.value,
        )

    @pytest.mark.asyncio
    async def test_base_service(self, base_service, request_data):
        await base_service.send(request_data)
        response = base_service.get_response()
        assert response.status == 200

    @pytest.mark.asyncio
    async def test_base_service_response(self, base_service, request_data):
        mock_data = 'Data'

        base_service.loads_data = AsyncMock()
        base_service.loads_data.return_value = mock_data

        await base_service.send(request_data)
        response = base_service.get_response()
        assert response.get_data() == mock_data
