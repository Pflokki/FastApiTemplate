from pydantic import Field
from pydantic.env_settings import BaseSettings
from enum import Enum


class Environment(Enum):
    PRODUCTION = 'prod'
    DEVELOPMENT = 'dev'
    LOCAL = 'local'
    TEST = 'test'


class CommonSettings(BaseSettings):

    ENVIRONMENT: str = Environment.PRODUCTION.value
    DEBUG: bool = False
    LOG_LEVEL: str = 'INFO'

    PG_SCHEMA_NAME: str = Field(..., env='DB_SCHEMA')
    PG_RW_DSN: str
    PG_POOL_SIZE: int = 50
    PG_POOL_SIZE_MAX_OVERFLOW: int = 10
    PG_POOL_RECYCLE: int = 1800
    PG_POOL_TITLE: int = 1

    BASE_SERVICE_TIMEOUT: int = 2
    BASE_SERVICE_RETRY_COUNT: int = 3

    logging_conf: dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'stdout': {
                'class': 'logging.Formatter',
                'format': '[%(asctime)s] appname=%(name)s | %(levelname)s: %(processName)s | message=%(message)s'
            },
        },
        'handlers': {
            'stdout': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'stdout',
            },
        },
        'loggers': {
            'gunicorn.error': {
                'handlers': ['stdout'],
                'level': 'WARNING',
                'propagate': False,
            },
            'uvicorn.error': {
                'handlers': ['stdout'],
                'level': 'WARNING',
                'propagate': False,
            },
            'gunicorn.access': {
                'handlers': ['stdout'],
                'level': LOG_LEVEL,
                'propagate': False,
            },
            'uvicorn.access': {
                'handlers': ['stdout'],
                'level': LOG_LEVEL,
                'propagate': False,
            },
            'app': {
                'handlers': ['stdout'],
                'level': LOG_LEVEL,
                'propagate': False,
            },
            'api_healthcheck': {
                'handlers': ['stdout'],
                'level': LOG_LEVEL,
                'propagate': False,
            },
            'http_service': {
                'handlers': ['stdout'],
                'level': LOG_LEVEL,
                'propagate': False,
            },
        }
    }

