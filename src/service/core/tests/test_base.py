import pytest
from unittest.mock import AsyncMock

from service.core.base import Base
from service.core.request_data import RequestData, RequestMethod
from service.core.response_data import ResponseData
from service.core.request_paginator.limit_offset_paginator import LimitOffsetParamsPaginator
from service.core.request_paginator.attribute_paginator import AttributePaginator, RequestAttributes
from service.core.request_policy import RequestPolicy
from aiohttp.client_exceptions import ClientConnectionError


class TestBaseService:
    @pytest.fixture(scope='function')
    def base_service(self) -> Base:
        rp = RequestPolicy(timeout=5, retry_count=0)
        return Base(policy=rp)

    @pytest.fixture(scope='function')
    def request_data(self) -> RequestData:
        return RequestData(
            'https://google.com/',
            RequestMethod.GET.value,
        )

    @pytest.fixture(scope='function')
    def paginator(self) -> RequestData:
        return RequestData(
            'https://google.com/',
            RequestMethod.GET.value,
        )

    @pytest.mark.asyncio
    async def test_base_service_retry(self, base_service: Base, request_data: RequestData):
        retry_count = 3

        base_service._send_request = AsyncMock(side_effect=ClientConnectionError)

        with pytest.raises(Exception):
            await base_service.send(request_data, request_policy=RequestPolicy(retry_count=retry_count))

        assert base_service._send_request.call_count == retry_count

    @pytest.mark.asyncio
    async def test_base_service_response_data(self, base_service: Base, request_data: RequestData):
        mock_data = 'Data'

        base_service.loads_data = AsyncMock()
        base_service.loads_data.return_value = mock_data

        await base_service.send(request_data)
        response = base_service.get_response()
        assert response.get_data() == mock_data

    @pytest.mark.asyncio
    async def test_base_service_limit_offset_paginator(self, base_service: Base, request_data: RequestData):
        paginator = LimitOffsetParamsPaginator(
            request_data=request_data,
            start_offset=10,
            max_offset=50,
            limit=10,
        )

        base_service._send_request = AsyncMock()
        base_service._send_request.return_value = ResponseData()

        await base_service.paginate(paginator)

        assert len(base_service._request_history) == 5

    @pytest.mark.asyncio
    async def test_base_service_attribute_paginator(self, base_service: Base):
        request_data = RequestData(
            '',
            RequestMethod.GET.value,
            params={'test_key': list(range(100))}
        )

        paginator = AttributePaginator(
            request_data=request_data,
            attribute_name=RequestAttributes.params,
            attribute_key='test_key',
            limit=10,
        )

        base_service._send_request = AsyncMock()
        base_service._send_request.return_value = ResponseData()

        await base_service.paginate(paginator)

        assert len(base_service._request_history) == 10
