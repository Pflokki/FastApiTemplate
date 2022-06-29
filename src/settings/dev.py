from settings.common import CommonSettings, Environment


class Settings(CommonSettings):

    ENVIRONMENT: str = Environment.DEVELOPMENT.value
    DEBUG: bool = True
    LOG_LEVEL: str = 'DEBUG'

