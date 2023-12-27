import typing
from abc import ABCMeta, abstractmethod
from psycopg import AsyncConnection

__all__ = ('ISession', 'ISessionPool', )


class ISession(metaclass=ABCMeta):

    @abstractmethod
    async def atomic(self) -> typing.AsyncIterator['ISession']:
        raise NotImplementedError

    @property
    @abstractmethod
    def connection(self) -> AsyncConnection[typing.Any]:
        """
        For ReadModels (Queries)
        """
        raise NotImplementedError


class ISessionPool(metaclass=ABCMeta):

    @abstractmethod
    async def session(self) -> typing.AsyncIterator[ISession]:
        raise NotImplementedError
