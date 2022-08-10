import pytest

from sqlalchemy import (
    Column,
    Integer,
    select,
    insert,
    delete,
    update,
)

from sqlalchemy.sql.functions import (
    max,
)

from database import (
    RWDatabase,
    Base,
)
from database.models.mixins import (
    IdentityIdMixin,
    CreatedAtDateMixin,
    CreatedAtDateTimeMixin,
    IsDeletedMixin,
)


class TestDatabaseIdentityIdModel(Base, IdentityIdMixin):
    __tablename__ = 'TestDatabaseIdentityIdModel'

    test_value = Column(Integer, default=1)


class TestDatabaseCreatedAtDateModel(Base, IdentityIdMixin, CreatedAtDateMixin):
    __tablename__ = 'TestDatabaseCreatedAtDateModel'

    test_value = Column(Integer, default=1)


class TestDatabaseCreatedAtDateTimeModel(Base, IdentityIdMixin, CreatedAtDateTimeMixin):
    __tablename__ = 'TestDatabaseCreatedAtDateTimeModel'

    test_value = Column(Integer, default=1)


class TestDatabaseIsDeletedModel(Base, IdentityIdMixin, IsDeletedMixin):
    __tablename__ = 'TestDatabaseIsDeletedModel'

    test_value = Column(Integer, default=1)


@pytest.mark.asyncio
async def test_database_identity_id_model():
    rw_database = RWDatabase(is_debug=True)

    Base.metadata.create_all(bind=rw_database.get_engine().sync_engine)

    session = rw_database.get_session()

    async with session.begin():
        insert_statement = (
            insert(TestDatabaseIdentityIdModel).
            values(
                [
                    dict(test_value=10),
                    dict(test_value=10),
                    dict(test_value=20),
                    dict(test_value=30),
                ]
            )
        )
        await session.execute(insert_statement)
        await session.commit()

        select_statement = (
            select(max(TestDatabaseIdentityIdModel.id))
        )
        database_value = await session.scalar(select_statement)

    assert database_value == 4


