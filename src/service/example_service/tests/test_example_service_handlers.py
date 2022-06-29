import pytest
from unittest.mock import patch

from service.example_service.handlers import get_alive_data
from service.example_service.schemas.alive_data import AliveData
from service.core.exceptions import ServiceUnavailable



@pytest.mark.asyncio
async def test_get_alive_data():
    data = await get_alive_data()
    assert isinstance(data, AliveData)


@pytest.mark.asyncio
async def test_get_alive_mocked_data():
    mocked_data = 'scqjjhj1klsjc'

    with patch('service.example_service.example_service.get_alive_data') as service_patch:
        service_patch.return_value = (200, mocked_data)
        data = await get_alive_data()

    assert data.data == mocked_data


@pytest.mark.asyncio
async def test_get_alive_mocked_exception():
    with patch('service.example_service.example_service.get_alive_data') as service_patch:
        service_patch.side_effect = ServiceUnavailable()
        data = await get_alive_data()

    assert data.data == 'Something went wrong'
