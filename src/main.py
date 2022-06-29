from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from logging import config

from api import api_router
from settings import settings


def init_middleware(app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    return app


def init_router(app: FastAPI) -> FastAPI:
    root_router = APIRouter()

    root_router.include_router(api_router)

    app.include_router(root_router)
    return app


def init_logging():
    config.dictConfig(settings.logging_conf)


def create_app() -> FastAPI:
    params = dict(
        title='FastAPI Template',
        description='',
        docs_url='/docs/',
    )
    app = FastAPI(**params)

    init_logging()
    app = init_middleware(app)
    app = init_router(app)

    return app


app = create_app()
