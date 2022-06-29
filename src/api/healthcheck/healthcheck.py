from fastapi import APIRouter

from api.healthcheck.schemas.healthcheck import ReadyItem

URL_HEALTHCHECK = '/healthcheck/'
URL_READY = '/ready/'
URL_LIVE = '/live/'

api_router = APIRouter()


@api_router.get(URL_HEALTHCHECK, response_model=list[ReadyItem])
async def healthcheck():
    return [
        ReadyItem(service='main'),
    ]


@api_router.get(URL_READY, response_model=list[ReadyItem])
async def ready():
    return [
        ReadyItem(service='main')
    ]


@api_router.get(URL_LIVE)
async def live():
    return ""
