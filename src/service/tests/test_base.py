import pytest
from unittest.mock import AsyncMock

from service.core.base import (
    Base,
    RequestMethod,
    RequestPolicy,
)


class TestBaseService:
    @pytest.fixture(scope='class')
    def base_service(self):
        rp = RequestPolicy(timeout=5, retry_count=0)
        return Base(policy=rp)

    @pytest.mark.asyncio
    async def test_base_service(self, base_service):
        await base_service.send(
            url='https://google.com/',
            method=RequestMethod.GET,
        )
        status, _ = base_service.get_response_data()
        assert status == 200

    @pytest.mark.asyncio
    async def test_base_service_response(self, base_service):
        mock_data = 'Data'

        base_service.loads_data = AsyncMock()
        base_service.loads_data.return_value = mock_data

        await base_service.send(
            url='https://google.com/',
            method=RequestMethod.GET,
        )
        status, data = base_service.get_response_data()
        assert data == mock_data
