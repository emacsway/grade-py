import typing
from functools import wraps
from collections.abc import Callable, Awaitable
from psycopg import AsyncConnection, AsyncTransaction

from ....infrastructure.seedwork.session.interfaces import ISession, IIdentityMap
from .identity_map import IdentityMap

__all__ = ('PgSession', )


class PgSession(ISession):
    _connection: AsyncConnection[typing.Any]
    _parent: typing.Optional['PgSession']
    _identity_map: IIdentityMap
    _transaction: typing.Optional[AsyncTransaction]

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

    async def __call__(self, func: Callable[['ISession'], Awaitable[typing.Any]]) -> typing.Any:
        @wraps(func)
        async def _decorated(*a, **kw):
            with self:
                return await func(*a, **kw)

        return _decorated

    async def __aenter__(self) -> 'ISession':
        ts = await self.connection.transaction()
        self._transaction = await ts.__aenter__()
        return PgTransactionSession(self._transaction.connection, self)

    async def __aexit__(self, exc_type, exc_value, traceback) -> bool:
        return await self._transaction.__aexit__(exc_type, exc_value, traceback)


# TODO: Add savepoint support
class PgTransactionSession(PgSession):

    async def __aenter__(self) -> 'ISession':
        return type(self)(self.connection, self)

    async def __aexit__(self, exc_type, exc_value, traceback) -> bool:
        return True
