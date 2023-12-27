import typing
from contextlib import asynccontextmanager
from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool

from ....application.seedwork.session import ISessionPool
from ..session.interfaces import ISession, IIdentityMap
from .identity_map import IdentityMap

__all__ = ('PgSession', 'PgSessionPool', )


class PgSessionPool(ISessionPool):
    _pool: AsyncConnectionPool

    def __init__(self, pool: AsyncConnectionPool):
        self._pool = pool

    @asynccontextmanager
    async def session(self) -> typing.AsyncIterator[ISession]:
        async with self._pool.connection() as conn:
            yield PgSession(conn)


class PgSession(ISession):
    _connection: AsyncConnection[typing.Any]
    _parent: typing.Optional['PgSession']
    _identity_map: IIdentityMap

    def __init__(self, connection, parent: typing.Optional['PgSession'] = None):
        self._connection = connection
        self._parent = parent
        self._identity_map = IdentityMap()

    @property
    def connection(self) -> AsyncConnection:
        return self._connection

    @property
    def identity_map(self) -> IIdentityMap:
        return self._identity_map

    @asynccontextmanager
    async def atomic(self) -> typing.AsyncIterator[ISession]:
        async with self.connection.transaction() as transaction:
            yield PgTransactionSession(transaction.connection, self)


# TODO: Add savepoint support
class PgTransactionSession(PgSession):

    @asynccontextmanager
    def atomic(self) -> typing.AsyncIterator[ISession]:
        yield PgTransactionSession(self._connection, self)

    @asynccontextmanager
    async def atomic2(self) -> typing.AsyncIterator[ISession]:
        async with self.connection.transaction() as transaction:
            yield PgTransactionSession(transaction.connection, self)
