from settings.common import CommonSettings, Environment


class Settings(CommonSettings):

    ENVIRONMENT: str = Environment.PRODUCTION.value
