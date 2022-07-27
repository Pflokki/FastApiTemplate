import pytest

from database import RWDatabase


@pytest.mark.asyncio
async def test_rw_database_initialising():
    select_value = 1
    rw_database = RWDatabase(is_debug=True)

    session = rw_database.get_session()

    value = await session.scalar(f'select {select_value}')

    assert value == select_value


