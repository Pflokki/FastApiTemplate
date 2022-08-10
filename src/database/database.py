from sqlalchemy import MetaData
from sqlalchemy.engine.url import make_url
from sqlalchemy.pool import QueuePool
from sqlalchemy.ext.asyncio.engine import create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import settings

metadata = MetaData(schema=settings.PG_SCHEMA_NAME)
Base = declarative_base(metadata=metadata)


class BaseDatabase:
    def __init__(
            self,
            database_dsn: str = settings.PG_RW_DSN,
            is_debug: bool = False
    ):
        self._engine_params: dict = {
            'poolclass': QueuePool,
            'pool_size': settings.PG_POOL_SIZE,
            'max_overflow': settings.PG_POOL_SIZE_MAX_OVERFLOW,
            'pool_recycle': settings.PG_POOL_RECYCLE,
            'pool_timeout': settings.PG_POOL_TITLE,
            'echo': is_debug,
        }

        self._engine_master: AsyncEngine = create_async_engine(
            make_url(database_dsn),
            **self._engine_params,
        )

        self._session_factory_args: dict = {
            'future': True,
            'autoflush': False,
            'class_': AsyncSession,
        }
        self._async_session_factory = sessionmaker(bind=self._engine_master, **self._session_factory_args)

    def get_session(self) -> AsyncSession:
        return self._async_session_factory()

    def get_engine(self) -> AsyncEngine:
        return self._engine_master

    async def shutdown(self):
        await self._engine_master.dispose()


class RWDatabase(BaseDatabase):
    def __init__(
            self,
            database_dsn: str = settings.PG_RW_DSN,
            is_debug: bool = False
    ):
        super(RWDatabase, self).__init__(database_dsn=database_dsn, is_debug=is_debug)
