import os
import importlib
from logging import getLogger, Logger

from settings.common import Environment, CommonSettings

env = os.environ.get('ENVIRONMENT', Environment.PRODUCTION.value)

if env == Environment.PRODUCTION.value:
    settings_module = importlib.import_module(f'settings.prod')
elif env == Environment.DEVELOPMENT.value:
    settings_module = importlib.import_module(f'settings.dev')
elif env == Environment.LOCAL.value:
    settings_module = importlib.import_module(f'settings.dev')
elif env == Environment.TEST.value:
    settings_module = importlib.import_module(f'settings.dev')
else:
    settings_module = importlib.import_module(f'settings.prod')


settings: CommonSettings = settings_module.Settings()


def get_logger(handler_name: str = '') -> Logger:
    if handler_name and handler_name in settings.logging_conf['loggers']:
        return getLogger(name=handler_name)
    else:
        return getLogger(name='app')
