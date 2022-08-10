from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Date,
    Boolean,
    Identity,
)


class IdentityIdMixin:
    id = Column(Integer, Identity(start=1, cache=100), primary_key=True)


class CreatedAtDateTimeMixin:
    created_at = Column(DateTime, default=datetime.now())


class CreatedAtDateMixin:
    created_at = Column(Date, default=datetime.now().date(), index=True)


class IsDeletedMixin:
    is_deleted = Column(Boolean, default=False, index=True)
