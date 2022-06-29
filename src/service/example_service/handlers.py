from service.example_service import example_service
from service.core.exceptions import ServiceUnavailable

from service.example_service.schemas.alive_data import AliveData


async def get_alive_data():
    try:
        _, data = await example_service.get_alive_data()
    except ServiceUnavailable:
        data = 'Something went wrong'
    return AliveData(
        data=data
    )
